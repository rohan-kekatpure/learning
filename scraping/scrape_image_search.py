from bs4 import BeautifulSoup
import re
import json

with open('round_pub_table.html') as f:
    doc = BeautifulSoup(f, 'html')

elems = doc.find_all('div', class_='rg_di')
ptrn = r'{.*}'
for e in elems:
    json_txt = re.findall(ptrn, e.text)[0]
    img_url = json.loads(json_txt)['ou']
    print(img_url)
    