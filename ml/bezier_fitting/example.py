import cv2
from aarwild_bpy.ops import spinbz
import aarwild_bpy.funcs as F

F.delete_default_objects()
F.change_units_to_inches()
img = cv2.imread('img/leg1.jpg')
spinbz('leg', img, steps=64)

