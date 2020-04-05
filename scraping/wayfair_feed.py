import requests
from pathlib import Path
import json

BASE_URL = 'http://apdev2.xwv7upzyan.us-west-2.elasticbeanstalk.com'

def clear_feed():
    response = requests.get('{}/list/feed'.format(BASE_URL)).json()
    feed_ids = response['data']

    for feed_id in feed_ids:
        payload = {'feed_id': feed_id}
        endpoint = '{}/delete/feed'.format(BASE_URL)
        response = requests.post(endpoint, json=payload)        
        print(response.json())


def clear_jobs():
    response = requests.get('{}/list/jobs'.format(BASE_URL)).json()
    job_ids = response['data']

    for job_id in job_ids:
        payload = {'job_id': job_id}
        endpoint = '{}/delete/job'.format(BASE_URL)
        response = requests.post(endpoint, json=payload)        
        print(response.json())

def populate_feed():
    # Recurse `wayfair_images` directory to get list of SKUs and corresponding images
    with open('./wayfair_pdp_image_urls.json') as f:
        assets = json.load(f)

    endpoint = '{}/create/feed'.format(BASE_URL)
    for asset in assets:
        sku = asset['sku']
        payload = {
                "sku": sku,
                "tag": "wayfair_pilot3",
                "client": "wayfair",
                "option_id": "default",
                "image_urls": asset['images']
            }

        
        response = requests.post(endpoint, json=payload)      
        print(response.json())
        

    # root_dir = Path('wayfair_images')
    # sku_dirs = root_dir.glob('*')
    # for sku_dir in sku_dirs:
    #     img_paths = sku_dir.glob('*.jpg')
    #     for img_pth in img_paths:

            

    # endpoint = '{}/create/feed'



if __name__ == '__main__':
    # clear_feed()
    # populate_feed()
    clear_jobs()