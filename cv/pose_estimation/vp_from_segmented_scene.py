import sys
from collections import namedtuple
import cv2
import numpy as np
np.set_printoptions(threshold=np.inf, floatmode='fixed', precision=2)
from scipy.interpolate import splprep, splev
from IPython import embed
from sklearn.linear_model import LinearRegression
from fspy import solve

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

class Line(dict):
    """
    Utility class for a 2D straight line
    """
    def __init__(self, slope, intercept):
        super().__init__(slope=slope, intercept=intercept)
        self.slope = slope
        self.intercept = intercept

    def __iter__(self):
        return iter([self.slope, self.intercept])

    def __str__(self):
        return 'Line({:0.4f}, {:0.4f})'.format(self.slope, self.intercept)

    def __repr__(self):
        return self.__str__()

    def eval(self, x):
        m, b = self
        return m * x + b


def _filter_by_color_limits(image,  color_low, color_high):
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

def _get_line_fit(x, y):
    lr = LinearRegression(fit_intercept=True, n_jobs=1)
    lr.fit(x.reshape(-1, 1), y)
    m, b = lr.coef_[0], lr.intercept_
    return Line(m, b)

def _get_intersection(line1, line2):
    m1, b1 = line1
    m2, b2 = line2
    # TODO: catch the condition if m1 == m2
    x_intersect = -(b2 - b1) / (m2 - m1)
    y_intersect = (m2 * b1 - m1 * b2) / (m2 - m1)
    return Point(x_intersect, y_intersect)

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

    # We now divide up the 4 quadrants into 5 regions as follows:
    # R1 : -pi to -pi/2 - eps
    # R2: -pi/2 - eps to -pi/2 + eps
    # R3: -pi/2 + eps to pi/2 - eps
    # R4: pi/2 - eps to pi/2 + eps
    # R5: pi/2 + eps to pi
    #
    # In other words, small angular regions around theta = -pi/2
    # and theta = +pi/2 are R2 and R4 respectively. We ignore
    # any points in R2 and R4 because they are clipped by image
    # boundaries. R1 and R5 are really a single region to the
    # left of the y-axis. We only include points from R3 and
    # R1 union R5 (R1u5). We fit a line to points belonging to R3
    # and fit a separate line to points in R1u5. The intersection of
    # these lines is the vanishing point.

    eps = 0.05  # Heuristic; angle tolerence
    p = np.pi
    # regions = [-p, -p/2 - eps, -p/2 + eps, p/2 - eps, p/2 + eps, p]
    # assignments = np.digitize(angles, regions)
    # Ra = assignments == 3
    # Rb = (assignments == 1) | (assignments == 5)

    regions = [-p, -p + eps, -p/2 - eps, -p/2 + eps, -eps, eps, p/2 - eps, p/2 + eps, p - eps, p]
    assignments = np.digitize(angles, regions)
    if wall in ['LEFT', 'RIGHT', 'FRONT']:
        Ra = (assignments == 4) | (assignments == 6)
        Rb = (assignments == 2) | (assignments == 8)
    elif wall in ['CEIL', 'FLOOR']:
        Ra = (assignments == 6) | (assignments == 8)
        Rb = (assignments == 2) | (assignments == 4)
    else:
        raise ValueError('Invalid wall: {}'.format(wall))

    if (x1[Ra].shape[0] == 0) or (x1[Rb].shape[0] == 0):
        embed()

    line_a = _get_line_fit(x1[Ra], y1[Ra])
    line_b = _get_line_fit(x1[Rb], y1[Rb])
    p_int = _get_intersection(line_a, line_b)
    return line_a, line_b, p_int

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
    pl.ylim([0, H])
    pl.axis('off')
    pl.show()

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
            wall_data['line1'] = line1
            wall_data['line2'] = line2
            wall_data['vp'] = vp

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

def _compute_vanishing_segments(scene, vp_walls):
    """
    Computes vanishing segments for the assigned walls
    in the scene. Even though the scene object already
    contains vanishing points explicitly, fSpy requires
    vanishing points to be represented as two segments
    (4 points). Therefore we need need to recompute the
    two-segment representation for the walls that are
    assigned by `_assign_vp_mode()`
    """
    vp = []
    for wall_type in vp_walls:
        img_size = scene['img_size']
        W = img_size['width']
        H = img_size['height']
        a = float(W) / float(H)
        wall_info = scene[wall_type]
        m1, b1 = wall_info['line1']
        m2, b2 = wall_info['line2']
        x11, x12 = 0.25, 0.75
        x21, x22 = 0.25, 0.75
        y11 = m1 * a * x11 + b1 / H
        y12 = m1 * a * x12 + b1 / H
        y21 = m2 * a * x21 + b2 / H
        y22 = m2 * a * x22 + b2 / H

        segment = [
            [{'x': x11, 'y': y11}, {'x': x12, 'y': y12}],
            [{'x': x21, 'y': y21}, {'x': x22, 'y': y22}]
        ]
        vp.append(segment)

    return vp

def compute_camera_parameters(orig_img_pth, segmented_img_pth):
    segmented_img = cv2.imread(segmented_img_pth)
    scene = _compute_scene(segmented_img)
    vp_mode, vp_walls = _assign_vp_mode(scene)
    vp = _compute_vanishing_segments(scene, vp_walls)
    params = solve(orig_img_pth, scene, vp, mode=vp_mode)
    print(params)
    # _visualize(img, scene)

def example():
    if len(sys.argv) < 2:
        print('Usage: python {} <image_path>'.format(sys.argv[0]))
        exit(1)
    segmented_img_path = sys.argv[1]
    orig_img_path = sys.argv[2]
    compute_camera_parameters(orig_img_path, segmented_img_path)

if __name__ == '__main__':
    example()
