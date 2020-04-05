from pathlib import Path
import requests

# place actual API KEY here
API_KEY = 'VdsfTdt5.pRbm8iYyCPq4xwV6ygT7oUdeGYvuBjMd'


def post_mesh():
    url1 = 'https://portal-test.aarwild.com:8443/api/meshlib/'
    headers_1 = {'authorization': 'Api-Key {}'.format(API_KEY)}
    payload = {
        "tags": ["2", "4"],
        "client": "Wayfair",
        "component_code": "1",
        "component_definition": "top"
    }
    response_1 = requests.post(url1, json=payload, headers=headers_1).json()
    print(response_1)


    meshlib_id = response_1['meshlib_id']
    meshlib_file_upload_url_tmpl = 'https://portal-test.aarwild.com:8443/api/meshlib/{meshlib_id}/upload_file/'
    upload_url = meshlib_file_upload_url_tmpl.format(meshlib_id=meshlib_id)
    headers_2 = {
        'authorization': 'Api-Key {}'.format(API_KEY),
        'accept': 'application/json'
    }

    # Specify file type
    data = {
        'type': 'mesh',
    }
    with Path('mesh.blend').open('rb') as f:
        files = {'file': f}
        response_2 = requests.post(upload_url, headers=headers_2, files=files, data=data)
    print(response_2.text)


if __name__ == '__main__':
    post_mesh()
