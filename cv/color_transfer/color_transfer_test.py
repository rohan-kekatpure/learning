from aarwild_utils.img import transfer_color_lab
import cv2

color_img = cv2.imread('color_1.jpg')
pattern_img = cv2.imread('pattern_3.jpg')
result = transfer_color_lab(color_img, pattern_img)
cv2.imwrite('result.jpg', result)
