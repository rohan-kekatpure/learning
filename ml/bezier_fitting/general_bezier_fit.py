import matplotlib.pyplot as pl
import numpy as np
from numpy.linalg import inv, pinv
from scipy.linalg import invpascal


def bezier_matrix(n):
    if n < 0:
        raise ValueError('Order = {}, has to be >0'.format(n))

    IPn = invpascal(n + 1, kind='lower', exact=False)
    Bn = np.abs(IPn[-1, :]).reshape(-1, 1)
    return Bn * IPn


def t_matrix(t, n):
    if n < 0:
        raise ValueError('Order = {}, has to be >0'.format(n))    
    return np.vander(t, n + 1, increasing=True)


def get_tvals(x, y):
    dx = x[1:] - x[:-1]
    dy = y[1:] - y[:-1]
    dvals = np.sqrt(dx * dx + dy * dy)
    dvals = np.hstack((0, dvals))
    dvals /= dvals.sum()
    tvals = np.cumsum(dvals)
    return tvals


def fit(x, y, fit_order):
    M = bezier_matrix(fit_order)
    tvals = get_tvals(x, y)
    T = t_matrix(tvals, fit_order)
    Q = inv(M) @ pinv(T.T @ T) @ T.T 
    Cx = Q @ x
    Cy = Q @ y
    C = np.vstack((Cx, Cy)).T
    return T, M, C


def f1(x):
    y1 = np.sin(x)
    y2 = np.sin(3 * x)
    return abs(y1*0 + y2)


def f2(x):
    return np.sin(x * x)


def main():

    # Create the dataset
    x = np.linspace(0, np.pi / 6, 100)
    y = f1(x)

    # Fitting 
    fit_order = 3
    T, M, C = fit(x, y, fit_order)
    xy_bz = T @ M @ C
    pl.plot(x, y, color='gray')
    # pl.plot(Cx, Cy, 'ro')
    pl.plot(xy_bz[:, 0], xy_bz[:, 1], 'b-')
    pl.show()


if __name__ == '__main__':
    main()
