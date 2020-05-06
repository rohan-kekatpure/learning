import json

from IPython import embed
from aarwild_utils.qds.solver import compute_camera_parameters as ccp_fspy

# from aarwild_utils.pose import compute_camera_parameters as ccp_awld
from pose import compute_camera_parameters as ccp_awld
import numpy as np
import sys
import cv2

if len(sys.argv) < 2:
    print('Usage: python {} <orig_img_path> <segm_img_path>'.format(sys.argv[0]))
    exit(1)

orig_img_path = sys.argv[1]
segm_img_path = sys.argv[2]

ccp_fspy(orig_img_path, segm_img_path)
with open('_camera_params.json') as f:
    dct = json.load(f)

try:
    params_fspy = np.array(dct['cameraParameters']['cameraTransform']['rows'])
except:
    params_fspy = None

segm_img = cv2.imread(segm_img_path)
# camera_matrix, focal_len = ccp_awld(segm_img, save_scene_visual=True)
camera_matrix, focal_len, scene = ccp_awld(segm_img, save_scene_visual=True)

print('\nfspy:')
print('=' * 40)
print(params_fspy)
print('\naarwild:')
print('=' * 40)
print(camera_matrix)
print('aarwild focal_len -> {:0.6f}'.format(focal_len))
print('-' * 40)

embed()
