import numpy as np
import matplotlib.pyplot as pl

def c1(u):
    return np.column_stack((u, 0.1 * np.sin(np.pi * u)))

def c3(u):
    return np.column_stack((0.5 + 2 * u, 1 + 0.2 * np.sin(np.pi * u / 2 )))

def c2(v):
    return np.column_stack((0.5 * v, v))

def c4(v):
    return np.column_stack((2.5 * v + 2, v))


def main():
    u = np.linspace(0, 2, 20)
    v = np.linspace(0, 1, 20)
    U, V = np.meshgrid(u, v)
    U = U.reshape(-1, 1)
    V = V.reshape(-1, 1)
    P12 = np.array([0, 0.])
    P14 = np.array([2., 0.])
    P23 = np.array([0.5, 1.])
    P34 = np.array([4.5, 1.])

    T1 = (1 - V) * c1(U) + V * c3(U)
    T2 = (1 - U) * c2(V) + U * c4(V)
    T3 = (1 - U) * (1 - V) * P12 + U * V * P34 + U * (1 - V) * P14 + (1 - U) * V * P23
    S = T1 + T2 - T3

    xy1 = c1(u)
    pl.plot(xy1[:, 0], xy1[:, 1], 'r-')

    xy2 = c3(u)
    pl.plot(xy2[:, 0], xy2[:, 1], 'b-')

    xy3 = c2(v)
    pl.plot(xy3[:, 0], xy3[:, 1], 'r-')

    xy4 = c4(v)
    pl.plot(xy4[:, 0], xy4[:, 1], 'b-')

    pl.plot(S[:, 0], S[:, 1], 'm.')
    pl.show()

if __name__ == '__main__':
    main()
