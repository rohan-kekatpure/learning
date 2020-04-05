import os
from functools import wraps
from pathlib import Path
import requests


def get_token_machine_to_machine(client_id, client_secret):
    url = 'https://aarwild-dev.auth0.com/oauth/token'
    header = {'content-type': 'application/json'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': 'https://pipeline-api.aarwild.com',
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=header, json=data).json()
    return response['access_token']


def get_client_id_and_secret():
    try:
        client_id = os.environ.get('AUTH0_CLIENT_ID')
        client_secret = os.environ.get('AUTH0_CLIENT_SECRET')
        return client_id, client_secret
    except KeyError:
        msg = 'Credentials not found;' \
              'please ensure that`AUTH0_CLIENT_ID` and ' \
              '`AUTH0_CLIENT_SECRET` are present in ' \
              'process environment'
        raise KeyError(msg)


def get_new_token(save=True, token_file='/tmp/token.txt'):
    client_id, client_secret = get_client_id_and_secret()
    token = get_token_machine_to_machine(client_id, client_secret)
    if save:
        with Path(token_file).open('w') as f:
            f.write(token)
    return token


def retry(func):
    @wraps(func)
    def ret_fn(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        if not isinstance(response, requests.models.Response):
            raise ValueError('Decorated function must return an instance of requests.models.Response')
        if response.json().get('code') == 'token_expired':
            self.token = get_new_token(save=True)
            response = func(self, *args, **kwargs)
        return response
    return ret_fn


class AuthRequests:
    def __init__(self, token):
        self.token = token

    def _get_header(self):
        return {'authorization': 'Bearer {}'.format(self.token)}

    @retry
    def get(self, url):
        response = requests.get(url, headers=self._get_header())
        return response

    @retry
    def post(self, url, data):
        response = requests.post(url, json=data, headers=self._get_header())
        return response

    @retry
    def foo(self):
        return 0


if __name__ == '__main__':
    tok_expired = open('token_expired.txt').read().strip()
    ar = AuthRequests(tok_expired)
    resp = ar.get('http://localhost:9000/list/material').json()
    resp2 = ar.foo()
    print(resp)



