import requests

endpoint = 'http://localhost:8000/api/products/detail/8d7284fa-ff58-46cd-befd-39dfa2d39399/'
response = requests.get(endpoint)
print(response.json())
print(response.status_code)