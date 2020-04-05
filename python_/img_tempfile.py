from tempfile import NamedTemporaryFile
import aarwild_utils.img as IMG
import cv2

url = 'https://st.hzcdn.com/simgs/22915a8608acc7a0_8-4400/asian-table-lamps.jpg'
with NamedTemporaryFile(dir='.', suffix='.jpg') as f:
    IMG.download_img(url, f.name)
    # img = IMG.url_to_image(url)    
    # cv2.imwrite(img, f.name)   
    print(f.name)

