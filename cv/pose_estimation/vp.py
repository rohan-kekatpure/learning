import cv2
import numpy as np
import matplotlib.pyplot as pl


img = cv2.imread('img/room4.jpg')

# Edge detection
edges = cv2.Canny(img, 100, 200, apertureSize=5, L2gradient=True)

# Hough transform
lines = cv2.HoughLinesP(edges, 10, 0.1, threshold=200, minLineLength=20, maxLineGap=2)

# Erosion
# kernel = np.ones((5, 5), dtype=np.uint8)
# erosion = cv2.erode(edges, kernel, iterations=1)

fig, ax = pl.subplots(2, 1, figsize=(10, 10))
ax[0].imshow(img, cmap='gray')
ax[1].imshow(edges, cmap='gray')

for line in lines:
    l = line[0]
    ax[1].plot([l[0], l[2]], [l[1], l[3]], 'g-')

pl.savefig('img.png')

