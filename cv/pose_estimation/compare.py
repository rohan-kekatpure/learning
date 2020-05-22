import json

from IPython import embed
from aarwild_quick_design.qds.solver import compute_camera_parameters as ccp_fspy
from aarwild_quick_design.scene import Scene
import aarwild_quick_design.vizutils as viz
import numpy as np
import sys
import cv2

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
scene = Scene(segm_img)
scene.build()
viz.draw_vps(scene)

headerprint('FOCAL LENGTH')
print('fspy -> {}'.format(dct['cameraParameters']['relativeFocalLength']))
print('aarwild -> {}'.format(scene.relative_focal_length))

headerprint('VANISHING POINTS')
print('fspy -> ')
for vp in dct['cameraParameters']['vanishingPoints']:
    print(vp)

print('\naarwild -> ')
for vp in scene.vanishing_points:
    print(vp)

headerprint('CAMERA MATRIX')
M_awld = scene.camera_matrix
print('fspy -> ')
M_fspy = np.array(dct['cameraParameters']['cameraTransform']['rows'])
print(M_fspy)
print('\naarwild -> ')
print(M_awld)

headerprint('DIFFERENCE (A - F)')
print(M_awld[:3, :3] - M_fspy[:3, :3])

headerprint('SIGN')
sgn = np.sign(M_awld * M_fspy)[:3, :3].astype(int)
print(sgn)

from IPython import embed; embed(); exit(0)
