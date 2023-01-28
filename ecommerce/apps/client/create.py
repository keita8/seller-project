import requests

endpoint = 'http://localhost:8000/api/products/create/'
data = {
    'title': 'un nouvel article',
    'category': 'basket',
    'content': 'description'
}
response = requests.post(endpoint, json=data)
print(response.json())
print(response.status_code)