import numpy as np
from collections import namedtuple
from scipy.interpolate import splprep, splev
from scipy.spatial.transform import Rotation as ROT
from sklearn.linear_model import LinearRegression, RANSACRegressor, TheilSenRegressor
import cv2

EPS = 1e-9
np.set_printoptions(threshold=np.inf, floatmode='fixed', precision=5, suppress=True)
np.random.seed(0)

# Ordering of wall types is important for the logic in this code
WALL_TYPES = ['LEFT', 'RIGHT', 'CEIL', 'FLOOR', 'FRONT']

COL_FLOOR = [119, 81, 81]
COL_CEIL = [210, 247, 241]
COL_FRONT_WALL = [93, 69, 249]
COL_LEFT_WALL = [170, 229, 255]
COL_RIGHT_WALL = [181, 206, 144]

COL_LEFT_LOW = (160, 220, 240)
COL_LEFT_HIGH = (180, 240, 255)
COL_RIGHT_LOW = (170, 195, 135)
COL_RIGHT_HIGH = (190, 215, 155)
COL_CEIL_LOW = (200, 235, 230)
COL_CEIL_HIGH = (220, 255, 250)
COL_FLOOR_LOW = (110, 70, 70)
COL_FLOOR_HIGH = (130, 90, 90)
COL_FRONT_LOW = (80, 60, 240)
COL_FRONT_HIGH = (100, 80, 255)

COLOR_LIMITS = {
    'LEFT': (COL_LEFT_LOW, COL_LEFT_HIGH),
    'RIGHT': (COL_RIGHT_LOW, COL_RIGHT_HIGH),
    'CEIL': (COL_CEIL_LOW, COL_CEIL_HIGH),
    'FLOOR': (COL_FLOOR_LOW, COL_FLOOR_HIGH),
    'FRONT': (COL_FRONT_LOW, COL_FRONT_HIGH),
}

Point = namedtuple('Point', ['x', 'y'])

DEFAULT_VP1 = Point(1, -0.15)
DEFAULT_VP2 = Point(-1.8, -0.15)
DEFAULT_FOCAL_LENGTH = 1.3333333333333333


class Line(dict):
    """
    Utility class for a 2D straight line
    """
    def __init__(self, slope, intercept, confidence=1.0):
        super().__init__(slope=slope, intercept=intercept)
        self.slope = slope
        self.intercept = intercept
        self.confidence = confidence

    def __iter__(self):
        return iter([self.slope, self.intercept])

    def __str__(self):
        return 'Line({:0.4f}, {:0.4f})'.format(self.slope, self.intercept)

    def __repr__(self):
        return self.__str__()

    def eval(self, x):
        m, b = self
        return m * x + b

def _visualize(img, scene):
    """
    Only used for debugging purposes, disable in prod
    """
    import matplotlib.pyplot as pl
    H, W = img.shape[:2]
    pl.imshow(img)
    colors = ['r', 'g', 'b', 'm', 'k']
    VPs = []
    for i, wall_type in enumerate(WALL_TYPES):
        if wall_type in ['CEIL', 'FLOOR', 'FRONT']:
            continue

        wall_data = scene[wall_type]
        color = colors[i]

        if not wall_data['present']:
            continue

        # Compute the lines of the wall
        x = np.linspace(0, W, 200)
        y1 = wall_data['line1'].eval(x)
        y2 = wall_data['line2'].eval(x)
        pl.plot(x, y1, '-', color=color, lw=2)
        pl.plot(x, y2, '-', color=color, lw=2)

        # Plot vanishing point
        vp = wall_data['vp']
        VPs.append(vp)
        pl.plot(vp[0], vp[1], '*', color=color, ms=10)

    if len(VPs) == 2:
        pl.plot([VPs[0].x, VPs[1].x], [VPs[0].y, VPs[1].y], 'k--', lw=2)

    pl.xlim([0, W])
    pl.ylim([H, 0])
    pl.axis('off')
    pl.savefig('_scene_visualization.png')


def _filter_by_color_limits(image, color_low, color_high):
    """
    Returns pixels that are between `color_low` and `color_high`.
    `color_low` and `color_high` are BGR tuples in OpenCV format.
    The return values is a binary image (mask).

    MOVE TO aarwild_utils.img
    """
    mask = cv2.inRange(image, color_low, color_high)
    return mask


def _get_largest_connected_component(nary_image):
    """
    Returns the largest connected component in `image`, which is
    assumed to be a nary, meaning it has only `n` distinct integer
    values, one corresponding to each separate component.
    """
    labels, counts = np.unique(nary_image, return_counts=True)
    max_label = 1 + np.argmax(counts[1:])  # ignore label = 0, which is background
    max_count = counts[max_label]
    return max_count, max_label


def _is_component_valid(comp_area, image_width, image_height, frac=0.05):
    """
    Returns True if component area is larger than frac * image_area.
    Any component whose area is less than frac * image_area cannot
    be a valid component.

    The reason this trivial logic gets its own function is that as
    the complexity of the task goes up, we may need extra validation
    logic. A function lets us put this logic in one place without
    changing the downstream code.
    """
    return comp_area > frac * image_width * image_height


def _compute_convex_hull(binary_image):
    """
    Computes convex hull of a binary image. For indoor scenes
    the walls are guaranteed to be convex, which is what lets
    us use this logic. If your 2D manifolds are NOT guaranteed
    to convex, canvex enclosure will give wrong answer.
    """
    contours, _ = cv2.findContours(
        binary_image,
        mode=cv2.RETR_EXTERNAL,
        method=cv2.CHAIN_APPROX_NONE
    )

    if len(contours) == 0:
        return np.array([])

    points = contours[0].reshape(-1, 2)
    hull = cv2.convexHull(points).reshape(-1, 2)

    # Make sure hull is closed
    hull = np.row_stack((hull, hull[0]))
    return hull


def _get_line_fit_simple(x, y):
    lr = LinearRegression(fit_intercept=True, n_jobs=1)
    x = x.reshape(-1, 1)
    lr.fit(x, y)
    m, b = lr.coef_[0], lr.intercept_
    confidence = lr.score(x, y)
    return Line(m, b, confidence)

def _get_line_fit_ransac(x, y):
    lr = LinearRegression()
    rr = RANSACRegressor(base_estimator=lr)
    x = x.reshape(-1, 1)
    try:
        rr.fit(x, y)
        m, b = rr.estimator_.coef_[0], rr.estimator_.intercept_
        mask = rr.inlier_mask_
        confidence = rr.score(x[mask], y[mask])
    except ValueError:
        lr.fit(x, y)
        m, b = lr.coef_[0], lr.intercept_
        confidence = lr.score(x, y)

    return Line(m, b, confidence)

def _get_line_fit_theilsen(x, y):
    tsr = TheilSenRegressor()
    x = x.reshape(-1, 1)
    tsr.fit(x, y)
    m, b = tsr.coef_[0], tsr.intercept_
    confidence = tsr.score(x, y)
    return Line(m, b, confidence)

def _get_intersection(line1, line2):
    m1, b1 = line1
    m2, b2 = line2
    # TODO: catch the condition if m1 == m2
    xi = -(b2 - b1) / (m2 - m1)
    yi = (m2 * b1 - m1 * b2) / (m2 - m1)
    return Point(xi, yi)

def _filter_points(x, y, side):
    return x, y

def _compute_line_params(p1, p2):
    """
    Given two points p1 = (x1, y1) and p2 = (x2, y2),
    the function computes the parameters for the
    line in the standard form ax + by + c = 0.
    """
    x1, y1 = p1
    x2, y2 = p2

    adx = abs(x2 - x1)
    ady = abs(y2 - y1)

    if (adx < EPS) and (ady < EPS):
        raise ValueError('Need two distinct points for a line, ({}, {}), ({}, {})'.format(x1, y1, x2, y2))

    if adx < EPS:
        return 1., 0., -x1

    if ady < EPS:
        return 0., 1., -y1

    slope = m = (y2 - y1) / (x2 - x1)
    return m, -1, (y1 - m * x1)


def _compute_closest_point(point, line):
    """
    Returns coordinates of the point on line `line` that
    is closest to the point `point`. Line is represented
    in terms of its parameters (a, b, c): ax + by + c = 0
    and point is point: (x0, y0)
    """
    x0, y0 = point
    a, b, c = line

    u = a * x0 + b * y0 + c
    lsq = a * a + b * b

    if lsq < EPS:
        raise ValueError('Not a line ({}, {}, {})'.format(a, b, c))

    dist = abs(u) / np.sqrt(lsq)

    v = b * x0 - a * y0
    cx = (b * v - a * c) / lsq
    cy = (-a * v - b * c) / lsq
    closest_pt = (cx, cy)
    return dist, closest_pt


def _compute_vp_from_poly4(hull, wall):
    """
    Computes vanishing point (VP) from the convex hull `hull`.
    The convex hull of wall is assumed to be a 4-gon (quadrilateral)
    """
    x0, y0 = hull[:, 0], hull[:, 1]
    n_points = 1000
    tck, _ = splprep([x0, y0], s=0, per=1, k=1)
    u1 = np.linspace(0, 1, n_points)
    x1, y1 = splev(u1, tck)
    dx = np.diff(x1, append=x1[-1])
    dy = np.diff(y1, append=y1[-1])
    angles = np.arctan2(dy, dx)

    # We now divide up the 4 quadrants into 9 regions as depicted
    # in ./pose_logic.jpg and fit lines to set of points which are
    # not horizontal or vertical

    eps_x = 0.05  # Heuristic; angle tolerence about x-axis (horizontal)
    eps_y = 0.10  # Heuristic; angle tolerence about y-axis (vertical)
    p = np.pi
    regions = [
        -p,
        -p + eps_x,
        -p / 2 - eps_y,
        -p / 2 + eps_y,
        -eps_x,
        eps_x,
        p / 2 - eps_y,
        p / 2 + eps_y,
        p - eps_x,
        p
    ]
    region = np.digitize(angles, regions)
    if wall == 'LEFT':
        Ra = (region == 4) | (region == 6)
        Rb = (region == 2) | (region == 8)
        xa, ya = _filter_points(x1[Ra], y1[Ra], 'LEFT')
        xb, yb = _filter_points(x1[Rb], y1[Rb], 'LEFT')
    elif wall == 'RIGHT':
        Ra = (region == 4) | (region == 6)
        Rb = (region == 2) | (region == 8)
        xa, ya = _filter_points(x1[Ra], y1[Ra], 'RIGHT')
        xb, yb = _filter_points(x1[Rb], y1[Rb], 'RIGHT')
    elif wall == 'FRONT':
        Ra = (region == 4) | (region == 6)
        Rb = (region == 2) | (region == 8)
        xa, ya = _filter_points(x1[Ra], y1[Ra], 'RIGHT')
        xb, yb = _filter_points(x1[Rb], y1[Rb], 'RIGHT')
    elif wall == 'CEIL':
        Ra = (region == 2) | (region == 4)
        Rb = (region == 6) | (region == 8)
        xa, ya = _filter_points(x1[Ra], y1[Ra], 'LEFT')
        xb, yb = _filter_points(x1[Rb], y1[Rb], 'RIGHT')
    elif wall == 'FLOOR':
        Ra = (region == 2) | (region == 4)
        Rb = (region == 6) | (region == 8)
        xa, ya = _filter_points(x1[Ra], y1[Ra], 'LEFT')
        xb, yb = _filter_points(x1[Rb], y1[Rb], 'RIGHT')
    else:
        raise ValueError('Invalid wall: {}'.format(wall))

    # For insufficient number of points, return lines with 0 confidence
    if (xa.shape[0] < 2) or (xb.shape[0] < 2):
        return Line(-1., -1., 0), Line(-1., -1., 0), Point(0, 0)

    line_a = _get_line_fit_ransac(xa, ya)
    line_b = _get_line_fit_ransac(xb, yb)
    p_int = _get_intersection(line_a, line_b)
    return line_a, line_b, p_int


def _compute_scene(segmented_img):
    """
    Computes scene info from the segmented image. Scene info
    is a large dictionary containing information about every
    wall found in the segmented image. The computed wall information
    includes presence, area fraction, vanishing lines, and
    vanishing point. An example scene info
    dictionary is below:

    {
      "img_size": (1000, 1024),
      "LEFT": {
        "present": true,
        "frac": 0.10804444444444444,
        "line1": {
          "slope": 0.6085912085025705,
          "intercept": 8.191525463296863
        },
        "line2": {
          "slope": -0.9146919935648665,
          "intercept": 361.84396656582277
        },
        "vp": [
          232.1646038126989,
          149.48486226918777
        ]
      },
      "RIGHT": {
        "present": true,
        "frac": 0.047822222222222224,
        "line1": {
          "slope": -0.3399272854756361,
          "intercept": 262.6780737743618
        },
        "line2": {
          "slope": 0.987671401400012,
          "intercept": -268.3573785682675
        },
        "vp": [
          399.9969701629945,
          126.7081895083761
        ]
      },
      "CEIL": {
        "present": true,
        "frac": 0.15413703703703704,
        "line1": {
          "slope": -0.44868160099867666,
          "intercept": 322.3868838317588
        },
        "line2": {
          "slope": 0.6064486465795312,
          "intercept": 9.743060715650913
        },
        "vp": [
          296.308274579091,
          189.43881280445675
        ]
      },
      "FLOOR": {
        "present": true,
        "frac": 0.3711925925925926,
        "line1": {
          "slope": 0.8990067401542693,
          "intercept": -220.11268477979291
        },
        "line2": {
          "slope": -0.8022267320474438,
          "intercept": 356.0939096030923
        },
        "vp": [
          338.6993048268481,
          84.38027314510894
        ]
      },
      "FRONT": {
        "present": true,
        "frac": 0.30666666666666664,
        "line1": {
          "slope": 0.009753618110430596,
          "intercept": 79.48569795024093
        },
        "line2": {
          "slope": -0.13748149945364022,
          "intercept": 311.54045703346105
        },
        "vp": [
          1576.0829544095634,
          94.85820919791101
        ]
      }
    }

    """
    img = segmented_img.copy()
    H, W = img.shape[:2]
    scene = dict.fromkeys(['img_size'] + WALL_TYPES)
    scene['img_size'] = {'height': H, 'width': W}
    scene['vanishing_points'] = None
    for i, wall_type in enumerate(WALL_TYPES):
        wall_data = dict.fromkeys(['present', 'frac', 'line1', 'line2', 'vp'])
        scene[wall_type] = wall_data

        # Initially a wall is assumed to be absent, will be changed
        # to true if detected
        wall_data['present'] = False

        low = COLOR_LIMITS[wall_type][0]
        high = COLOR_LIMITS[wall_type][1]
        mask = _filter_by_color_limits(img.copy(), low, high)
        n_comps, comp_map = cv2.connectedComponents(mask, connectivity=4)

        if n_comps == 1:  # Wall not found
            continue
        else:
            max_area, max_label = _get_largest_connected_component(comp_map)
            wall_data['frac'] = max_area / (W * H)

        # If the largest component has a very small area it is invalid
        # In this case, found no  component at all, the component map
        # is zeroed out
        if not _is_component_valid(max_area, W, H, frac=0.02):
            comp_map *= 0

        # In case there are multiple components detected, zero out
        # all but the dominant component (zero out = make background)
        if n_comps > 2:
            comp_map[comp_map != max_label] = 0

        # Convert comp_map to uint8 for all further processing
        comp_map = comp_map.astype(np.uint8)

        # Take convex hull of the comp_map
        hull = _compute_convex_hull(comp_map)
        if len(hull) > 0:
            wall_data['present'] = True
            line1, line2, vp = _compute_vp_from_poly4(hull, wall_type)
            vp = _px2img(vp, W, H)  # Convert VP to image coordinates [-1, 1] x [-1, 1]
            wall_data['line1'] = line1
            wall_data['line2'] = line2
            wall_data['vp'] = vp
            wall_data['confidence'] = min(line1.confidence, line2.confidence)

    return scene


def _assign_vp_mode(scene):
    room_type = set()
    for wt in WALL_TYPES:
        if scene[wt]['present']:
            room_type.add(wt)

    if room_type == {'LEFT', 'RIGHT', 'CEIL', 'FLOOR', 'FRONT'}:
        vp_mode = '1vp'
        vp_walls = ['LEFT']
    elif room_type == {'LEFT', 'RIGHT', 'CEIL', 'FLOOR'}:
        vp_mode = '2vp'
        vp_walls = ['LEFT', 'RIGHT']
    elif room_type == {'RIGHT', 'LEFT', 'CEIL', 'FRONT'}:
        vp_mode = '1vp'
        vp_walls = ['CEIL']
    elif room_type == {'RIGHT', 'LEFT', 'FLOOR', 'FRONT'}:
        vp_mode = '1vp'
        vp_walls = ['FRONT']
    else:
        vp_mode = 'default'
        vp_walls = []

    return vp_mode, vp_walls


def _dist(p1, p2):
    """
    Computes distance between p1: (x1, y1) and p2: (x2, y2)
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    return np.sqrt(dx * dx + dy * dy)


def _px2img(point, image_width, image_height):
    W = float(image_width)
    H = float(image_height)
    x, y = point

    # Convert from absolute pixel coords to relative coords
    # [0, W] x [0, H] -> [0, 1], [0, 1]
    x /= W
    y /= H

    # Convert from relative to image plane coords
    a = W / H
    if a < 1.:  # [0, 1], [0, 1] -> [-a, a] x [-1, 1]
        u = a * (2 * x - 1)
        v = 1 - 2 * y
    else:  # [0, 1], [0, 1] -> [-1, 1] x [-1/a, 1/a]
        u = 2 * x - 1
        v = (1 - 2 * y) / a

    return Point(u, v)


def _compute_rotation_matrix(vp1, vp2, principal_pt, focal_length):
    """
    Computes the world->Camera rotation matrix M

    M takes a 3D world point (uw) to camera coordinate system

    M . uw = uc
    """
    f = focal_length
    Fu, Fv = vp1, vp2
    xc, yc = principal_pt
    Fui = Fu[0] - xc
    Fuj = Fu[1] - yc
    Fvi = Fv[0] - xc
    Fvj = Fv[1] - yc
    uc = np.array([Fui, Fuj, f])
    vc = np.array([Fvi, Fvj, f])
    uc /= np.linalg.norm(uc)
    vc /= np.linalg.norm(vc)
    wc = np.cross(uc, vc)
    M_W2C = np.row_stack((uc, vc, wc)).T
    return M_W2C


def _convert_to_axis_angle(rot_mtx):
    """
    Returns the axis-angle representation of rotation matrix
    """
    M = rot_mtx
    u = np.array([
        M[2, 1] - M[1, 2],
        M[0, 2] - M[2, 0],
        M[1, 0] - M[0, 1]
    ]).T
    u /= np.linalg.norm(u)
    t = np.trace(M)
    theta = np.arccos(0.5 * (t - 1.0))
    return u, theta


def _compute_focal_length(Fu, Fv, principal_point):
    P = principal_point
    horizon_line = _compute_line_params(Fu, Fv)
    PPuv, Puv = _compute_closest_point(P, horizon_line)
    PuvFu = _dist(Fu, Puv)
    FvPuv = _dist(Fv, Puv)
    OPuv = np.sqrt(PuvFu * FvPuv)
    focal_len = np.sqrt(OPuv ** 2 - PPuv ** 2)
    return focal_len


def _compute_vp2(vp1, principal_point, focal_length=DEFAULT_FOCAL_LENGTH):
    horizon = (1, 0)
    f = focal_length
    Fu = vp1
    xu, yu = Fu
    k = -(xu ** 2 + yu ** 2 + f ** 2) / (xu * horizon[0] + yu * horizon[1])
    xv = xu + k * horizon[0]
    yv = yu + k * horizon[1]
    Fv = Point(xv, yv)
    return Fv


def _align_to_axes(M, vp_mode):
    # Transformation to match to fspy
    x180 = ROT.from_rotvec([np.pi, 0, 0]).as_matrix()
    y180 = ROT.from_rotvec([0, np.pi, 0]).as_matrix()
    z180 = ROT.from_rotvec([0, 0, np.pi]).as_matrix()
    x90 = ROT.from_rotvec([np.pi / 2, 0, 0]).as_matrix()
    y90 = ROT.from_rotvec([0, np.pi / 2, 0]).as_matrix()
    z90 = ROT.from_rotvec([0, 0, np.pi / 2]).as_matrix()
    xn90 = ROT.from_rotvec([-np.pi / 2, 0, 0]).as_matrix()
    yn90 = ROT.from_rotvec([0, -np.pi / 2, 0]).as_matrix()
    zn90 = ROT.from_rotvec([0, 0, -np.pi / 2]).as_matrix()

    M = z180 @ M @ z180

    return M

def _compute_rot_matrix(vp1, vp2, principal_point, focal_length):
    Fu, Fv = vp1, vp2
    P = principal_point
    f = focal_length
    R = _compute_rotation_matrix(Fu, Fv, P, f)
    return R


def compute_camera_parameters(segmented_img, save_scene_visual=False):
    scene = _compute_scene(segmented_img)
    vp_mode, vp_walls = _assign_vp_mode(scene)
    principal_point = Point(0, 0)

    # Assign vp1, vp2 and focal length
    confidence = 0.0
    if vp_mode == '2vp':
        wall1, wall2 = vp_walls
        vp1 = scene[wall1]['vp']
        vp2 = scene[wall2]['vp']
        focal_len = _compute_focal_length(vp1, vp2, principal_point)
        confidence = min(scene[wall1]['confidence'], scene[wall2]['confidence'])
    elif vp_mode == '1vp':
        wall = vp_walls[0]
        vp1 = scene[wall]['vp']
        focal_len = DEFAULT_FOCAL_LENGTH
        vp2 = _compute_vp2(vp1, principal_point, focal_len)
        print(vp2)
        confidence = scene[wall]['confidence']
    elif vp_mode == 'default':
        vp1 = DEFAULT_VP1
        vp2 = DEFAULT_VP2
        focal_len = DEFAULT_FOCAL_LENGTH
        confidence = 1.0
    else:
        raise ValueError('Invalid vp_mode {}'.format(vp_mode))

    scene['vanishing_points'] = [vp1, vp2]
    print('vp1 -> {}'.format(vp1))
    print('vp2 -> {}'.format(vp2))
    if confidence < 0.8:
        vp1 = DEFAULT_VP1
        vp2 = DEFAULT_VP2
        focal_len = DEFAULT_FOCAL_LENGTH

    # Compute rotation matrix
    R = _compute_rot_matrix(vp1, vp2, principal_point, focal_len)
    R = R.T.copy()
    R = _align_to_axes(R, vp_mode)

    # Compute translation vector. In fSpy, this is simple 10 times the
    # third column of the rotation matrix. Thats what we'll be using
    # here to maintain parity
    default_dist = 10.0

    T = default_dist * R[:, -1]
    C = np.column_stack((R, T))
    C = np.row_stack((C, [0, 0, 0, 1.]))

    if save_scene_visual:
        _visualize(segmented_img, scene)

    print('vp_mode -> {}, confidence -> {:0.4f}'.format(vp_mode, confidence))
    return C, focal_len, scene
