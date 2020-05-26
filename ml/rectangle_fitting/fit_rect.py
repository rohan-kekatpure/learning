from pathlib import Path

import numpy as np
import matplotlib.pyplot as pl
from scipy.interpolate import splprep, splev

from scipy.optimize import minimize

def loss_function(x, hull):
    a, b, c, d = x
    X = hull[:, 0]
    Y = hull[:, 1]
    dist_from_bounds = np.abs(np.column_stack((X - a, X - b, Y - c, Y - d)))
    dist = np.min(dist_from_bounds, axis=1)
    loss = dist.mean()
    return loss


def conf(deviation, deviation_thresh, confidence_thresh):
    CT = confidence_thresh
    DT = deviation_thresh
    B = -np.log(CT) / DT
    return np.exp(-B * deviation)

def main():
    hull_files = Path('./hulls').glob('*.npy')
    for hull_file in hull_files:
        hull = np.load(hull_file)
        X = hull[:, 0]
        Y = hull[:, 1]
        n_points = 1000
        tck, _ = splprep([X, Y], s=0, per=1, k=1)
        u1 = np.linspace(0, 1, n_points)
        X1, Y1 = splev(u1, tck)
        hull1 = np.column_stack((X1, Y1))

        a0, b0 = X1.min(), X1.max()
        c0, d0 = Y1.min(), Y1.max()
        x0 = np.array([a0, b0, c0, d0])
        sol = minimize(loss_function, x0, args=(hull1, ), method='Nelder-Mead')
        if not sol.success:
            return
        # from IPython import embed; embed(); exit(0)
        a, b, c, d = sol.x
        pl.close('all')
        _, ax = pl.subplots(nrows=1, ncols=1)
        ax.plot(X1, Y1, '+')
        ax.plot([a, b], [c, c], 'r-')
        ax.plot([a, b], [d, d], 'r-')
        ax.plot([a, a], [c, d], 'r-')
        ax.plot([b, b], [c, d], 'r-')
        confidence = conf(sol.fun, 6.0, 0.8)
        ax.text(0.5, 0.5, 'DEV = {:0.2f}'.format(sol.fun), transform=ax.transAxes)
        ax.text(0.5, 0.6, 'CONF = {:0.2f}'.format(confidence), transform=ax.transAxes)

        file_name = Path('./{}.png'.format(hull_file.stem))
        pl.ylim([d0 * 1.2, 0])
        pl.savefig(file_name)

if __name__ == '__main__':
    main()
