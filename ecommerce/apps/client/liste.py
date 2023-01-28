import email
import requests
import json
from getpass import getpass

password = getpass("Mot de passe : ")
auth_endpoint = 'http://localhost:8000/api/auth/'
auth_response = requests.post(auth_endpoint, json={'username':'admin@gmail.com', 'password': password})
print(auth_response.json())
# print(response.text)
print(auth_response.status_code)


if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    endpoint = 'http://localhost:8000/api/products/'
    response = requests.get(endpoint, headers=headers)
    deserialized_response = json.loads(response.text)
    # print(response.json())
    data = response.json()
    next_url = data['next']
    results = data['results']
    print('next_url', next_url)
    print(f"Données desérialisée {deserialized_response} ")
    print(len(deserialized_response))
    print(response.status_code)
