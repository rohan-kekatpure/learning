import argparse
from pathlib import Path
import numpy as np
import cv2
from aarwild_quick_design.scene import Scene
import aarwild_quick_design.vizutils as viz

np.set_printoptions(threshold=np.inf, floatmode='fixed', precision=5, suppress=True)

def _process_args():
    parser = argparse.ArgumentParser(description='Wall estimation')

    parser.add_argument('-s', '--segmented-image', dest='segm_img_pth', action='store',
                        help='Path to segmented image', required=True)

    args = parser.parse_args()
    return args

def main():
    args = _process_args()

    segm_img_pth = Path(args.segm_img_pth)

    if not segm_img_pth.exists():
        print('Segmented image not found')
        exit(1)

    segm_img = cv2.imread(segm_img_pth.as_posix())
    scene = Scene(segm_img)
    scene.build()

    # viz.draw_vps(scene, savefig=False)
    viz.draw_walls(scene, savefig=False)


if __name__ == '__main__':
    main()
