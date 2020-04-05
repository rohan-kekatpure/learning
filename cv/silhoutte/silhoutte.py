import numpy as np
import cv2
import os

def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def get_rzcurve(img):    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, 100, 200)
    edges[edges > 0] = 1.0  # Threshold

    h, w = edges.shape
    rz_raw = []
    for i in range(h):
        nonzero_idx = np.nonzero(edges[i])[0]
        if nonzero_idx.shape[0] == 0:
            continue

        min_idx = nonzero_idx[0]
        max_idx = nonzero_idx[-1]
        avg = 0.5 * (min_idx + max_idx)
        r = max_idx - avg
        rz_raw.append(r)

    Z = range(len(rz_raw))
    R = np.array(list(reversed(rz_raw)))
    R = smooth(R, box_pts=5)
    RZ = np.vstack((R, Z)).T
    return RZ

if __name__ == '__main__':
    base_dir = '/Users/rohan/work/code/wayfair/lamp_stems/'
    img_list = os.listdir(base_dir)
    output_dir = './rz_curves'
    for img_name in img_list:
        if not img_name.endswith('.png'):
            continue

        print(img_name)
        img_filename = os.path.join(base_dir, img_name)
        img = cv2.imread(img_filename)
        try:
            rz_mat = get_rzcurve(img)            
        except:
            pass
        npy_filename = os.path.join(output_dir, img_name.split('.')[0] + '.npy')
        np.save(npy_filename, rz_mat)
    
