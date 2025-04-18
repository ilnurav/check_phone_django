import requests

response = requests.get(
    'http://localhost:8000/api/check_phone/',
    params={'phone': '79191534411'}
)
print(response.json())