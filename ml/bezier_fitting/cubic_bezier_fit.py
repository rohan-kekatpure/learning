import cv2
import matplotlib.pyplot as pl
import numpy as np
from scipy.interpolate import interp1d
from aarwild_utils.img import get_rz


def arclen_param(x, y):
    dx = np.diff(x)
    dy = np.diff(y)
    dvals = np.sqrt(dx * dx + dy * dy)
    arclen = dvals.sum()
    dvals /= arclen
    tvals = np.cumsum(dvals)
    tvals = np.insert(tvals, 0, 0)
    return arclen, tvals


def fit_fast(x, y):
    theta1 = np.arctan2(y[1] - y[0], x[1] - x[0])
    theta2 = np.arctan2(y[-1] - y[-2], x[-1] - x[-2])
    L, t = arclen_param(x, y)
    f = L / 3.
    cx1 = x[0] + f * np.cos(theta1)
    cy1 = y[0] + f * np.sin(theta1)
    cx2 = x[-1] - f * np.cos(theta2)
    cy2 = y[-1] - f * np.sin(theta2)
    control_points = np.array([
        [x[0], y[0]],
        [cx1, cy1],
        [cx2, cy2],
        [x[-1], y[-1]]
    ])
    return control_points


def bz_eval_single(bz_points, t):
    """
    Evaluation of single cubic bezier for supplied parameter values.
    :param bz_points: ndarray, 4 x 2, set of four control points of the cubic bezier
    :param t: ndarray, arclength parameter
    """
    M = np.array([
        [1., 0., 0., 0.],
        [-3., 3., 0., 0.],
        [3., -6., 3., 0.],
        [-1., 3., -3., 1.]
    ])
    T = np.vander(t, 4, increasing=True)
    C = bz_points
    return T @ M @ C


def bz_eval(bz_curves):
    """
    Bezier curve evaluation by chaining multiple bezier curves
    :param bz_curves: list, list of bezier curves, (bezier curve = 4x2 array of control points)
    :param splits: list, array indices of segment beginnings and end points.
                   E.g. i'th segment is between t[splits[i]] and t[splits[i + 1]]
    """
    X = np.array([], dtype=np.float)
    Y = np.array([], dtype=np.float)
    t = np.linspace(0, 1, 20)
    for i in range(len(bz_curves)):
        x, y = bz_eval_single(bz_curves[i], t).T
        X = np.hstack((X, x))
        Y = np.hstack((Y, y))

    return np.column_stack((X, Y))


def eval_error(bz_curves, x, y):
    x_fit, y_fit = bz_eval(bz_curves).T
    interp_func = interp1d(x_fit, y_fit, kind='linear', fill_value='extrapolate')
    y_fit_interp = interp_func(x)
    e = y_fit_interp - y
    error = np.sqrt(np.sum(e * e))
    return error


def fit_recursive(x, y, tol):
    bz = fit_fast(x, y)
    error = eval_error([bz], x, y)
    if error < tol:
        return [bz]
    mid = len(x) // 2
    end = len(x)
    result = fit_recursive(x[: mid + 1], y[: mid + 1], tol)
    result.extend(fit_recursive(x[mid: end + 1], y[mid: end + 1], tol))
    return result


def bz_plot(bz_curves, ax):
    for curve in bz_curves:
        # Plot points
        for point in curve:
            ax.plot(point[0], point[1], 'ro', ms=2)

        # Plot handles
        (x1, x2, x3, x4), (y1, y2, y3, y4) = curve.T
        ax.plot([x1, x2], [y1, y2], 'r-')
        ax.plot([x3, x4], [y3, y4], 'r-')


def _tester(x, y):
    tol = .1
    bz_curves = fit_recursive(x, y, tol)
    x_fit, y_fit = bz_eval(bz_curves).T

    plot = True
    if plot:
        fig, ax = pl.subplots()
        ax.plot(x, y, '-', color='gray')
        ax.plot(x_fit, y_fit, 'g-')
        bz_plot(bz_curves, ax)
        ax.set_aspect('equal')
        pl.show()


def test_fit_fast():
    x = np.linspace(0.2, 2, 50) * np.pi
    y = x * np.sin(x)
    _tester(x, y)
    _tester(y, x)


if __name__ == '__main__':
    img = cv2.imread('./img/vase1.jpg')
    rz = get_rz(img)
    max_error = 1
    rz_approx = cv2.approxPolyDP(rz.astype(int), max_error, closed=False)[:, 0, :]
    rz_approx = rz_approx.astype(float)
    ar, az = rz_approx.T
    bz = fit_recursive(az, ar, tol=0.1)
    bz = np.array(bz)
    z_fit, r_fit = bz_eval(bz).T

    # Plotting
    plot = True
    if plot:
        fig, ax = pl.subplots()
        ax.plot(rz[:, 1], rz[:, 0], 'k-')
        ax.plot(z_fit, r_fit, 'g-')
        bz_plot(bz, ax)
        pl.show()




