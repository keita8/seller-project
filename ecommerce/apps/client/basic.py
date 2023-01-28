import requests

endpoint = 'http://localhost:8000/'
response = requests.post(endpoint, json={'query':'hello'})
print(response.json())
print(response.status_code)