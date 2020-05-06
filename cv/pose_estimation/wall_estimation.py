import json
import numpy as np
import cv2
import matplotlib.pyplot as pl
from IPython import embed
from matplotlib.lines import Line2D

np.set_printoptions(threshold=np.inf, floatmode='fixed', precision=2, suppress=True)

def draw_box(ax, points):
    x0, x1, x2, x3, x4, x5, x6, x7 = points[0, :]
    y0, y1, y2, y3, y4, y5, y6, y7 = points[1, :]
    lines = [
        Line2D([x0, x1], [y0, y1], color='r', marker='*', markersize=7),
        Line2D([x1, x2], [y1, y2], color='r'),
        Line2D([x2, x3], [y2, y3], color='r'),
        Line2D([x3, x0], [y3, y0], color='r'),

        Line2D([x4, x5], [y4, y5], color='b'),
        Line2D([x5, x6], [y5, y6], color='b'),
        Line2D([x6, x7], [y6, y7], color='b'),
        Line2D([x7, x4], [y7, y4], color='b'),

        Line2D([x0, x4], [y0, y4], color='g'),
        Line2D([x1, x5], [y1, y5], color='g'),
        Line2D([x2, x6], [y2, y6], color='g'),
        Line2D([x3, x7], [y3, y7], color='g'),
    ]
    for line in lines:
        ax.add_line(line)


def get_cube2(origin, scale, camera_mtx, view_mtx, proj_mtx, img_width, img_height):
    o, s = origin, scale
    W, H = img_width, img_height
    C, V, P = camera_mtx, view_mtx, proj_mtx

    cube_w = np.array([
        [0., 0., 0.],
        [s[0], 0., 0.],
        [s[0], s[1], 0.],
        [0., s[1], 0.],
        [0., 0., s[2]],
        [s[0], 0., s[2]],
        [s[0], s[1], s[2]],
        [0., s[1], s[2]]
    ]).T

    cube_w += o
    cube_w = np.row_stack((cube_w, np.ones(cube_w.shape[1])))

    cube_c = V @ cube_w
    cube_p = P @ cube_c
    cube_p /= cube_p[3, :]

    # Cube in normalized pixel coords
    cube_npx = cube_p[:2, :]
    # embed()
    # Cube in absolute pixel coordinates
    a = float(img_width) / float(img_height)
    dims = np.array([[W, H]]).T
    cube_px = cube_npx * dims + dims // 2
    return cube_px


def _get_proj_matrix(focal_len, image_width, image_height, sensor_width=36., sensor_height=24.):
    # Defaults from Blender
    near = 0.1
    far = 100.0
    f_rel = focal_len
    wi = float(image_width)
    hi = float(image_height)
    ws = float(sensor_width)
    hs = float(sensor_height)
    a = wi / hi
    f_abs = f_rel * ws / a
    theta_x = np.arctan(ws / (2 * f_abs))
    theta_y = np.arctan(hs / (2 * f_abs))

    if image_height > image_width:
        hn = np.tan(0.5 * theta_y)
        wn = a * hn
    else:
        wn = np.tan(0.5 * theta_x)
        hn = wn / a

    u = (near + far) / (near - far)
    v = 2 * near * far / (near - far)
    proj_mtx = np.array([
        [1./wn, 0, 0, 0],
        [0, 1./hn, 0, 0],
        [0, 0, u, v],
        [0, 0, 1., 0]
    ])

    # proj_mtx = np.array([
    #     [1., 0, 0, 0],
    #     [0, 1., 0, 0],
    #     [0, 0, 1./f_rel, 0],
    #     [0, 0, 1./f_rel, 0]
    # ])

    return proj_mtx

def main():
    with open('_camera_params.json') as f:
        params = json.load(f)['cameraParameters']

    C = np.array(params['cameraTransform']['rows'])
    V = np.array(params['viewTransform']['rows'])
    print(V)
    f_rel = params['relativeFocalLength']
    print('f_rel -> {}'.format(f_rel))
    W = params['imageWidth']
    H = params['imageHeight']

    # Projection matrix
    P = _get_proj_matrix(f_rel, W, H)

    # Create a cube in world coords
    a = np.array([1, 1, 1])
    o = np.array([[0, 0, -1]]).T
    cube = get_cube2(o, a, C, V, P, W, H)

    # Plotting
    img = cv2.imread('scene17.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fig, ax = pl.subplots(1, 1)
    ax.imshow(img)
    # pl.plot(cube[0, :], cube[1, :], '*')
    draw_box(ax, cube)
    pl.show()


if __name__ == '__main__':
    main()
