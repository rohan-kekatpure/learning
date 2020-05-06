import json

from IPython import embed
from aarwild_utils.qds.solver import compute_camera_parameters as ccp_fspy

# from aarwild_utils.pose import compute_camera_parameters as ccp_awld
from pose import compute_camera_parameters as ccp_awld
import numpy as np
import sys
import cv2
from scipy.spatial.transform import Rotation as ROT

def headerprint(str_):
    print('\n')
    print('=' * 40)
    print(str_)
    print('=' * 40)


if len(sys.argv) < 2:
    print('Usage: python {} <orig_img_path> <segm_img_path>'.format(sys.argv[0]))
    exit(1)

orig_img_path = sys.argv[1]
segm_img_path = sys.argv[2]

ccp_fspy(orig_img_path, segm_img_path)
with open('_camera_params.json') as f:
    dct = json.load(f)

segm_img = cv2.imread(segm_img_path)
M_awld, focal_len, scene = ccp_awld(segm_img, save_scene_visual=False)

headerprint('FOCAL LENGTH')
print('fspy -> {}'.format(dct['cameraParameters']['relativeFocalLength']))
print('\naarwild -> {}'.format(focal_len))

headerprint('VANISHING POINTS')
print('fspy -> ')
for vp in dct['cameraParameters']['vanishingPoints']:
    print(vp)

print('\naarwild -> ')
for vp in scene['vanishing_points']:
    print(vp)

headerprint('CAMERA MATRIX')
print('fspy -> ')
M_fspy = np.array(dct['cameraParameters']['cameraTransform']['rows'])
print(M_fspy)
print('\naarwild -> ')
print(M_awld)

headerprint('DIFFERENCE (A - F)')
print(M_awld - M_fspy)
headerprint('SIGN')
sgn = np.sign(M_awld * M_fspy)[:3, :3].astype(int)
print(sgn)
# embed()
