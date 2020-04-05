import cv2
import numpy as np
import os
import sys


def get_img_stats(img):    
    mu = img.mean(axis=(0, 1))
    std = img.std(axis=(0, 1))
    return mu, std


def transfer_color_1(src=None, tgt=None):
    err_msg = 'function requires 3-channel images'
    assert src.ndim == 3, err_msg
    assert tgt.ndim == 3, err_msg

    src = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(float)
    tgt = cv2.cvtColor(tgt, cv2.COLOR_BGR2LAB).astype(float)

    mu_src, std_src = get_img_stats(src)
    mu_tgt, std_tgt = get_img_stats(tgt)

    # If source or target images is a solid color, 
    # just change the means
    EPS = 1.0e-9
    std_src[std_src < EPS] = 1.0
    std_tgt[std_tgt < EPS] = 1.0

    scaling = std_src / std_tgt    
    tgt_new = scaling * (tgt - mu_tgt) + mu_src
    tgt_new = np.clip(tgt_new, 0, 255)
    tgt_new = tgt_new.astype('uint8')    
    tgt_new_bgr = cv2.cvtColor(tgt_new, cv2.COLOR_LAB2BGR)
    return tgt_new_bgr

if __name__ == '__main__':
    extensions = ['jpg', 'JPG', 'png', 'PNG']

    color_img_name = None
    for ext in extensions:
        cname = 'color.{}'.format(ext)
        if os.path.exists(cname):
            color_img_name = cname

    pattern_img_name = None
    for ext in extensions:
        pname = 'pattern.{}'.format(ext)
        if os.path.exists(pname):
            pattern_img_name = pname

    if color_img_name is None:
        print('Color image not found')
        sys.exit(1)

    if pattern_img_name is None:
        print('Pattern image not found')
        sys.exit(1)

    cimg = cv2.imread(color_img_name)
    pimg = cv2.imread(pattern_img_name)
    result = transfer_color(src=cimg, tgt=pimg)
    cv2.imwrite('result.jpg', result)





