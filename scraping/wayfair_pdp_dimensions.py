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


class text_exist:
    def __init__(self, class_name):
        self.class_name = class_name        

    def __call__(self, driver):
        elems = driver.find_elements_by_class_name(self.class_name)        
        text = [e.text for e in elems]
        for t in links:
            if not link.startswith('https'):
                return False

        return links           


def get_elements_by_class_name(driver, url, class_name):
    timeout = 10
    wait = WebDriverWait(driver, timeout)

    # Synchronous search
    driver.get(url)    
    try:    
        expectation = links_exist(class_name)
        links = wait.until(expectation)
        return links
    except TimeoutException:
        return []

# def get_pdp_image_urls():

#     options = Options()
#     options.headless = True
#     driver = webdriver.Firefox(options=options)

#     df = pd.read_csv('/Users/rohan/Downloads/sku_list.csv')
#     columns = ['SKU', 'PDP']
#     df = df[columns]
#     i = 0
#     img_links = []

#     try:
#         for _, (sku, url) in df.iterrows():
#             print('\nrow -> {}, sku -> {}, url -> {}'.format(i, sku, url))
#             links = get_images_from_pdp(driver, url)
#             print('\n'.join(links))
#             sku_data = {'sku': sku, 'pdp_url': url, 'images': links}
#             img_links.append(sku_data)
#             time.sleep(5)
#             i += 1
#     except:
#         pass
#     finally:
#         with open('wayfair_pdp_image_urls.json', 'w') as f:
#             json.dump(img_links, f, indent=2)


def main():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    df = pd.read_csv('/Users/rohan/Downloads/sku_list.csv')
    columns = ['SKU', 'PDP']
    df = df[columns]
    i = 0
    img_links = []
    class_name = 'ProductWeightsDimensions-descriptionListItem'    
    # class_name = 'pl-Box--p-2 pl-DescriptionList-details'

    for _, (sku, url) in df.iterrows():
        driver.get(url)
        time.sleep(5)
        print('\nrow -> {}, sku -> {}, url -> {}'.format(i, sku, url))
        elems = driver.find_elements_by_class_name(class_name)
        # import ipdb; ipdb.set_trace()
        text = [e.text for e in elems]
        print(text)
        # import ipdb; ipdb.set_trace()

    
if __name__ == '__main__':
    main()
    # download_pdp_images()

