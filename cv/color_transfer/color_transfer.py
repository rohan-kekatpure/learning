import cv2
import numpy as np
import matplotlib.pyplot as pl
from aarwild_utils.img import fit_to_vgg
import argparse
import sys
import os


def get_img_stats(img):    
    mu = img.mean(axis=(0, 1))
    std = img.std(axis=(0, 1))
    return mu, std


def _to_mpl(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    return img 


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


def transfer_color_2(src=None, tgt=None):
    err_msg = 'function requires 3-channel images'
    assert src.ndim == 3, err_msg
    assert tgt.ndim == 3, err_msg

    src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    tgt = cv2.cvtColor(tgt, cv2.COLOR_BGR2HSV)

    mu_src, _ = get_img_stats(src)
    mu_tgt, _ = get_img_stats(tgt)

    tgt[..., 0] = tgt[..., 0] - mu_tgt[0] + mu_src[0]
    tgt_new = cv2.cvtColor(tgt, cv2.COLOR_HSV2BGR)
    return tgt_new


def create_gallery():
    images = ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg']
    pairs = [(s, t) for s in images for t in images if s != t]
    N = len(pairs)    
    fig, axes = pl.subplots(nrows=N, ncols=3, figsize=(24, 96))
    axes = axes.ravel()

    i = 0
    for src_, tgt_ in pairs:
        src_img = cv2.imread(src_)
        tgt_img = cv2.imread(tgt_)
        new_tgt_img = transfer_color_1(src=src_img, tgt=tgt_img)


        axes[i].imshow(_to_mpl(src_img))
        axes[i].axis('off')
        axes[i].text(0.05, 0.8, 'color', color='w', transform=axes[i].transAxes, fontsize=30)

        axes[i + 1].imshow(_to_mpl(tgt_img))
        axes[i + 1].axis('off')
        axes[i + 1].text(0.05, 0.8, 'pattern', color='w', transform=axes[i + 1].transAxes, fontsize=30)

        axes[i + 2].imshow(_to_mpl(new_tgt_img))
        axes[i + 2].axis('off')
        axes[i + 2].text(0.05, 0.8, 'result', color='w', transform=axes[i + 2].transAxes, fontsize=30)        

        i += 3

    pl.subplots_adjust(wspace=0, hspace=0.1)    
    pl.savefig('colors.jpg')


def commandline_app():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-c', '--color-image', dest='col_img',
                        action='store', help='Color image')

    parser.add_argument('-p', '--pattern-image', dest='pat_img',
                        action='store', help='Pattern image')    

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()        

    src = cv2.imread(args.col_img)
    tgt = cv2.imread(args.pat_img)    
    res = transfer_color_1(src, tgt)
    cv2.imwrite('xfer.jpg', res)


def windows_app():
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
    result = transfer_color_1(src=cimg, tgt=pimg)
    cv2.imwrite('result.jpg', result)


if __name__ == '__main__':
    windows_app()

        