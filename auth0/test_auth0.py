import requests


# client_id and client_secret for test API
AUTH0_CLIENT_ID = '1BmntiDrb7qb7trkgCvm1ykQFUdBcvYu'
AUTH0_CLIENT_SECRET = 'F3MNnMrz-7n-GMkwpEe4dQYkG1NZ8hSIvQhu3zTVDSaO3xVmuMDwuEhjtFcf7sLI'


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
    print(response)


def get_token_username_and_passwd(username, passwd, client_id, client_secret):
    url = 'https://aarwild-dev.auth0.com/oauth/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'password',
        'username': username,
        'password': passwd,
        'audience': 'https://pipeline-api.aarwild.com',
        'scope': 'read:sample',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(url, headers=header, data=data).json()
    print(response)


if __name__ == '__main__':
    # get_token_machine_to_machine(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET)
    get_token_username_and_passwd(
        'test@localhost.localdomain',
        'eBib8did',
        AUTH0_CLIENT_ID,
        AUTH0_CLIENT_SECRET
    )
