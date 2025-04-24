import requests

BASE_URL = "https://petstore.swagger.io/v2"

def create_pet(pet_data):
    url = f"{BASE_URL}/pet"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=pet_data)
    return response

def get_pet_by_id(pet_id):
    url = f"{BASE_URL}/pet/{pet_id}"
    response = requests.get(url)
    return response

def update_pet(pet_data):
    url = f"{BASE_URL}/pet"
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, json=pet_data)
    return response

def delete_pet_by_id(pet_id):
    url = f"{BASE_URL}/pet/{pet_id}"
    response = requests.delete(url)
    return response