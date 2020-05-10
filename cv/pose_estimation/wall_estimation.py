from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as pl
from IPython import embed
from matplotlib.lines import Line2D
from aarwild_quick_design.mathutils import img_to_px, Point
from aarwild_quick_design.scene import Scene
import argparse

np.set_printoptions(threshold=np.inf, floatmode='fixed', precision=2, suppress=True)

def _process_args():
    parser = argparse.ArgumentParser(description='Wall estimation')

    parser.add_argument('-s', '--segmented-image', dest='segm_img_pth', action='store',
                        help='Path to segmented image', required=True)

    parser.add_argument('-i', '--orig-image', dest='orig_img_pth', action='store',
                        help='path to original image', required=True)
    args = parser.parse_args()
    return args

def draw_box(ax, points):
    x0, x1, x2, x3, x4, x5, x6, x7 = points[0, :]
    y0, y1, y2, y3, y4, y5, y6, y7 = points[1, :]
    linestyle1 = '-'
    linestyle2 = '--'
    lines = [
        Line2D([x0, x1], [y0, y1], color='r', linestyle=linestyle1, marker='*'),
        Line2D([x1, x2], [y1, y2], color='g', linestyle=linestyle1),
        Line2D([x2, x3], [y2, y3], color='r', linestyle=linestyle1),
        Line2D([x3, x0], [y3, y0], color='g', linestyle=linestyle1, marker='*'),

        Line2D([x4, x5], [y4, y5], color='r', linestyle=linestyle2),
        Line2D([x5, x6], [y5, y6], color='g', linestyle=linestyle2),
        Line2D([x6, x7], [y6, y7], color='r', linestyle=linestyle2),
        Line2D([x7, x4], [y7, y4], color='g', linestyle=linestyle2),

        Line2D([x0, x4], [y0, y4], color='b', linestyle=linestyle1, marker='*'),
        Line2D([x1, x5], [y1, y5], color='b', linestyle=linestyle1),
        Line2D([x2, x6], [y2, y6], color='b', linestyle=linestyle2),
        Line2D([x3, x7], [y3, y7], color='b', linestyle=linestyle2),
    ]
    for line in lines:
        ax.add_line(line)


def get_unit_cube(origin, scale):
    cube_3d = np.array([
        [-1., -1, -1],
        [1., -1, -1],
        [1., 1, -1],
        [-1., 1, -1],
        [-1., -1, 1],
        [1., -1, 1],
        [1., 1, 1],
        [-1., 1, 1]
    ]).T

    cube_3d *= scale
    cube_3d += origin
    return cube_3d

def _project(points_3d, view_matrix, focal_len, image_width, image_height):
    V = view_matrix
    P = _get_projection_matrix(focal_len)
    W, H = image_width, image_height
    points_4d = np.row_stack((points_3d, np.ones(points_3d.shape[1])))

    points_cam = V @ points_4d
    points_proj = P @ points_cam
    points_proj /= points_proj[3, :]
    cube_imgplane = points_proj[:2, :]

    # Convert to pixel coords
    cube_px = np.zeros(cube_imgplane.shape)
    for i in range(cube_imgplane.shape[1]):
        px = img_to_px(Point(cube_imgplane[0, i], cube_imgplane[1, i]), W, H)
        cube_px[:, i] = [px.x, px.y]

    return cube_px

def _get_projection_matrix(focal_len):
    near = 0.01
    far = 10.
    f_rel = focal_len
    fov_x = 2. * np.arctan(1. / f_rel)
    s = 1. / np.tan(0.5 * fov_x)
    u = (near + far) / (near - far)
    v = 2 * near * far / (near - far)
    proj_mtx = np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, u, v],
        [0, 0, -1., 0]
    ])

    return proj_mtx

def main():
    args = _process_args()

    segm_img_pth = Path(args.segm_img_pth)
    orig_img_pth = Path(args.orig_img_pth)

    if not segm_img_pth.exists():
        print('Segmented image not found')
        exit(1)

    segm_img = cv2.imread(segm_img_pth.as_posix())
    scene = Scene(segm_img)
    scene.build()
    f_rel = scene.relative_focal_length
    V = scene.view_transform
    print('f_rel -> {}'.format(f_rel))
    W = scene.image_data['width']
    H = scene.image_data['height']

    # Create a cube in world coords
    o = np.array([[0., 0., -0.3]]).T
    fov = 2 * np.arctan(1. / f_rel)
    l = np.linalg.norm(V[:3, 3])
    s = np.tan(0.5 * fov)
    a = .4 * s * l
    cube_3d = get_unit_cube(o, a)
    cube_p = _project(cube_3d, V, f_rel, W, H)

    # Plotting
    img_rgb = cv2.cvtColor(segm_img, cv2.COLOR_BGR2RGB)
    fig, ax = pl.subplots(1, 1)
    ax.imshow(img_rgb)
    draw_box(ax, cube_p)
    pl.show()


if __name__ == '__main__':
    main()
