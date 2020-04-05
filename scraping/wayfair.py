import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import json
from pathlib import Path
import shutil
import wget


class links_exist:
    def __init__(self, class_name):
        self.class_name = class_name        

    def __call__(self, driver):
        elems = driver.find_elements_by_class_name(self.class_name)        
        links = [e.find_elements_by_css_selector('*')[1].get_attribute('src') for e in elems]
        for link in links:
            if not link.startswith('https'):
                return False

        return links           


def get_images_from_pdp(driver, url):
    timeout = 10
    wait = WebDriverWait(driver, timeout)
    class_name = 'ProductImageWithHoverZoom'

    # Synchronous search
    GLOBAL_driver.get(url)    
    try:    
        expectation = links_exist(class_name)
        links = wait.until(expectation)
        return links
    except TimeoutException:
        return []

def get_pdp_image_urls():

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    df = pd.read_csv('/Users/rohan/Downloads/sku_list.csv')
    columns = ['SKU', 'PDP']
    df = df[columns]
    i = 0
    img_links = []

    try:
        for _, (sku, url) in df.iterrows():
            print('\nrow -> {}, sku -> {}, url -> {}'.format(i, sku, url))
            links = get_images_from_pdp(driver, url)
            print('\n'.join(links))
            sku_data = {'sku': sku, 'pdp_url': url, 'images': links}
            img_links.append(sku_data)
            time.sleep(5)
            i += 1
    except:
        pass
    finally:
        with open('wayfair_pdp_image_urls.json', 'w') as f:
            json.dump(img_links, f, indent=2)


def download_pdp_images():
    with open('./wayfair_pdp_image_urls.json') as f:
        pdp_assets = json.load(f)

    # Create clean directory to store images
    img_dir = Path('./wayfair_images')
    if img_dir.exists():
        shutil.rmtree(img_dir)
    img_dir.mkdir()

    # download and store images
    sku_counts = {}
    for asset in pdp_assets:
        time.sleep(5)
        sku = asset['sku']
        sku_counts[sku] = 0
        sku_dir = img_dir / sku        
        if sku_dir.exists():
            sku_counts[sku] += 1
            sku_dir = img_dir / '{}_{}'.format(sku, sku_counts[sku])
        
        sku_dir.mkdir()

        img_num = 1
        for url in asset['images']:
            print('\nsku -> {}, url -> {}'.format(sku, url))
            img_path = sku_dir / 'img_{}.jpg'.format(img_num)
            wget.download(url, img_path.as_posix())
            img_num += 1

    


if __name__ == '__main__':
    # main()
    download_pdp_images()

