import sys

import numpy as np
import matplotlib.pyplot as pl
import matplotlib.lines as mlines
import cv2
from scipy.spatial.transform import Rotation as ROT
from IPython import embed


EPS = 1e-9
PIXEL_PER_MM_IPHONE6 = 1000.0 / 1.5

def get_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    dx1 = x1 - x2
    dy1 = y1 - y2
    dx2 = x3 - x4
    dy2 = y3 - y4

    det = dx1 * dy2 - dx2 * dy1

    if abs(det) < EPS:
        print('Warning: lines do not intersect')
        return (np.inf, np.inf)

    u1 = x1 * y2 - x2 * y1 
    u2 = x3 * y4 - x4 * y3

    px = (u1 * dx2 - u2 * dx1) / det
    py = (u1 * dy2 - u2 * dy1) / det  

    return (px, py)


def draw_lines(points1, points2, p_intersect, ax, color):    
    p1, p2 = points1
    p3, p4 = points2
    kwargs = dict(linewidth=2, color=color)
    l1 = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], **kwargs)
    l2 = mlines.Line2D([p3[0], p4[0]], [p3[1], p4[1]], **kwargs)    
    ax.add_line(l1)
    ax.add_line(l2)
    xi, yi = p_intersect
    ax.scatter(xi, yi, marker='x', color=color, s=10)    


def compute_line_params(p1, p2):
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
    

def compute_closest_point(point, line):
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
    cx = (b * v  - a * c) / lsq
    cy = (-a * v - b * c) / lsq
    closest_pt = (cx, cy)
    return dist, closest_pt
    

def dist(p1, p2):
    """
    Computes distance between p1: (x1, y1) and p2: (x2, y2)    
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    return np.sqrt(dx * dx + dy * dy)


def compute_rotation_matrix(Fu, Fv, principal_pt, focal_length):
    """
    Computes the world->Camera rotation matrix M

    M takes a 3D world point (uw) to camera coordinate system

    M . uw = uc

    All computations in pixel-coordinates
    """
    f = focal_length
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

def convert_to_axis_angle(rot_mtx):
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


def main():

    # # IMG_6209.JPG
    # p1 = (1840, 800)
    # p2 = (2448, 326)
    # p3 = (1800, 1802)
    # p4 = (2429, 2175)
    #
    # p5 = (1087, 777)
    # p6 = (1680, 798)
    # p7 = (1075, 2329)
    # p8 = (1539, 2337)

    # IMG_6210.JPG
    p1 = (4, 652)
    p2 = (524, 800)
    p3 = (116, 2580)
    p4 = (352, 2448)

    p5 = (2444, 2708)
    p6 = (276, 2284)
    p7 = (2444, 2080)
    p8 = (1500, 1976)

    # Get intersection point
    Fu = get_intersection(p1, p2, p3, p4)
    # print('{:0.2f}, {:0.2f}'.format(*Fu))

    Fv = get_intersection(p5, p6, p7, p8)
    # print('{:0.2f}, {:0.2f}'.format(*Fv))

    # Compute the params of line passing through pi1 and pi2
    a, b, c = horizon_line = compute_line_params(Fu, Fv)
    # print(horizon_line)

    # Read the image 
    img = cv2.imread(sys.argv[1])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    print(img.shape)
    # Compute closest distance and closest point on horizon line to principal point
    H, W = img.shape
    P = Px, Py = W // 2, H // 2
    d_P_Puv, Puv = compute_closest_point(P, horizon_line)

    d_Fu_Puv = dist(Fu, Puv)
    d_Fv_Puv = dist(Fv, Puv)
    d_O_Puv = np.sqrt(d_Fu_Puv * d_Fv_Puv)

    focal_length_px = np.sqrt(d_O_Puv ** 2 - d_P_Puv ** 2)
    focal_length_mm = focal_length_px / PIXEL_PER_MM_IPHONE6
    print('Estimated focal length = {:0.2f} px, {:0.2f} mm'.format(focal_length_px, focal_length_mm))

    # Rotation matrix
    R = compute_rotation_matrix(Fu, Fv, P, focal_length_px)
    rot = ROT.from_rotvec([np.pi, 0, 0]).as_matrix()
    R = rot @ R

    # Get axis-angle representation or rotation matrix
    axis, angle = convert_to_axis_angle(R)
    print('axis -> {}'.format(axis))
    print('angle -> {}'.format(angle * 180 / np.pi))

    # # Draw lines
    # _, ax = pl.subplots()
    # draw_lines([p1, p2], [p3, p4], Fu, ax, 'red')
    # draw_lines([p5, p6], [p7, p8], Fv, ax, 'green')
    # ax.imshow(img, cmap='gray')
    #
    # # Plot horizon line
    # xh = np.linspace(0, 3200, 50)
    # yh = a * xh + c
    # ax.plot(xh, yh, 'k--')
    # ax.set_xlim([0, img.shape[1]])
    # ax.set_ylim([img.shape[0], 0])
    #
    # # Plot principal point and closest point on horizon line
    # pl.scatter(Px, Py, color='w', s=20)
    # pl.scatter(Puv[0], Puv[1], color='#00ffff', s=20)
    # pl.show()


if __name__ == '__main__':
    main()

