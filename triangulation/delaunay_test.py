import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as pl

points = np.random.random(size=(100, 2))
tri = Delaunay(points)
pl.triplot(points[:, 0], points[:, 1], tri.simplices)
pl.plot(points[:, 0], points[:, 1], 'o')
pl.show()
