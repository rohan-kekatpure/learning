import numpy as np
import cv2
from aarwild_utils.img import get_rz
import matplotlib.pyplot as pl
import sys

if len(sys.argv) < 2:
    print('Usage: Python vase.py /path/to/image/file')
    sys.exit(1)

img = cv2.imread(sys.argv[1])
rz = get_rz(img)
rz_idx = np.fliplr(rz).astype(int).T
rz_img = np.zeros(img.shape[:2], dtype=np.uint8)
rz_img[rz_idx[0, :], rz_idx[1, :]] = 255

# Approximate the curve
max_error = 1
arz = cv2.approxPolyDP(rz.astype(int), max_error, closed=False)[:, 0, :]

# Calculate the angles
drz = np.diff(arz, axis=0, prepend=0)
theta = np.arctan2(drz[:, 1], drz[:, 0])
dtheta = np.diff(theta, prepend=0)
corner_idx = np.where(np.abs(dtheta) > .5)
corner_idx = (corner_idx[0] - 1, )
corner_rz = arz[corner_idx]

# Plotting
fig, ax = pl.subplots()
# ax.plot(rz[:, 0], rz[:, 1], 'g-')
ax.plot(arz[:, 0], arz[:, 1], 'r-', ms=5, mfc='none')
ax.plot(corner_rz[:, 0], corner_rz[:, 1], 'mo', ms=3)
ax.set_aspect('equal')
pl.show()
g = np.column_stack((arz, drz, theta, dtheta))
np.savetxt('vals.txt', g, fmt='%0.2f')

# pl.plot(rz[:, 0], rz[:, 1], 'go', ms=7, mfc=(0, 1, 0, 0.), mec='g')
# pl.plot(arz[:, 0], arz[:, 1], 'r+', ms=5)
# pl.show()


