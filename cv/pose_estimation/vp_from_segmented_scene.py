import sys
import cv2
import numpy as np
import matplotlib.pyplot as pl
from IPython import embed

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

def mask_part(img, part, fill_holes=True, keep_only_largest_component=True):
    im = img.copy()
    im[np.abs(img - part) > 5] = 0
    im[im > 0] = 255
    gray = im[:, :, 0]
    kernel = np.ones((3, 3), np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations=3)
    if fill_holes or keep_only_largest_component:
        try:
            im2, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        except:
            contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if fill_holes:
            for h, cnt in enumerate(contours):
                cv2.drawContours(gray, [cnt], 0, 255, -1)
            try:
                im2, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            except:
                contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if keep_only_largest_component:
            max_area = 0.0
            for h, cnt in enumerate(contours):
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
            for h, cnt in enumerate(contours):
                area = cv2.contourArea(cnt)
                if area < max_area:
                    cv2.drawContours(gray, [cnt], 0, 0, -1)
    return gray

def test_mask(img):
    gray = mask_part(img, COL_CEIL)
    _, ax = pl.subplots(2, 1, figsize=(6, 12))
    ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax[1].imshow(gray, cmap='gray')
    pl.show()

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
        method=cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) == 0:
        return np.array([])
        # raise ValueError('No contours could be extracted from binary image')

    points = contours[0].reshape(-1, 2)
    hull = cv2.convexHull(points).reshape(-1, 2)

    # Make sure hull is closed
    hull = np.row_stack((hull, hull[0]))

    return hull


def main():
    if len(sys.argv) < 2:
        print('Usage: python {} <image_path>'.format(sys.argv[0]))
        exit(1)

    img = cv2.imread(sys.argv[1])
    f = 600.0 / img.shape[1]
    img = cv2.resize(img, None, fx=f, fy=f)
    H, W = img.shape[:2]

    _, ax = pl.subplots(2, 3)
    ax = ax.ravel()

    walls = ['LEFT', 'RIGHT', 'CEIL', 'FLOOR', 'FRONT']
    limits = {
        'LEFT': (COL_LEFT_LOW, COL_LEFT_HIGH),
        'RIGHT': (COL_RIGHT_LOW, COL_RIGHT_HIGH),
        'CEIL': (COL_CEIL_LOW, COL_CEIL_HIGH),
        'FLOOR': (COL_FLOOR_LOW, COL_FLOOR_HIGH),
        'FRONT': (COL_FRONT_LOW, COL_FRONT_HIGH),
    }

    ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    for i, wall in enumerate(walls):
        low = limits[wall][0]
        high = limits[wall][1]
        mask = _filter_by_color_limits(img.copy(), low, high)
        n_comps, comp_map = cv2.connectedComponents(mask, connectivity=4)

        if n_comps == 1:  # Wall not found
            max_area = W * H
            max_label = 0
        else:
            max_area, max_label = _get_largest_connected_component(comp_map)

        # If the largest component has a very small area it is invalid
        # In this case, found no  component at all, the component map
        # is zeroed out
        if not _is_component_valid(max_area, W, H, frac=0.05):
            comp_map *= 0

        # In case there are multiple components detected, zero out
        # all but the dominant component (zero out = make background)
        if n_comps > 2:
            comp_map[comp_map != max_label] = 0

        # Convert comp_map to uint8 for all further processing
        comp_map = comp_map.astype(np.uint8)

        # Take convex hull of the comp_map
        hull = _compute_convex_hull(comp_map)

        # Filter new image with the comp_map as the mask
        new_img = cv2.bitwise_and(img, img, mask=comp_map)

        print('{}, frac = {}'.format(wall, max_area / (W * H)))
        curr_ax = ax[i + 1]
        curr_ax.imshow(cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB))

        if len(hull) > 0:
            curr_ax.plot(hull[:, 0], hull[:, 1], '-', color='#41fdfe', lw=2)

        curr_ax.text(0.5, 0.5, wall, fontsize=15, color='green', transform=curr_ax.transAxes)

        # exit(0)

    for a in ax:
        a.axis('off')
    pl.show()

if __name__ == '__main__':
    main()
