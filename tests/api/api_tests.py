import json
from random import random

from models.api.api_models import create_pet, delete_pet_by_id, get_pet_by_id, update_pet

with open('data/api/valid_data_api.json')as f:
    pet_data = json.load(f)

class TestPetstoreAPI:

    def test_create_pet_positive(self):
        response = create_pet(pet_data)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
        created_pet = response.json()
        assert created_pet['name'] == pet_data['name']
        assert created_pet['id'] == pet_data['id']

    def test_create_pet_negative_invalid_data(self):
        response = create_pet(None)
        assert response.status_code == 405, f"Expected status code 405, got {response.status_code}. Response: {response.text}"

    def test_delete_pet_by_id_positive(self):
        create_response = create_pet(pet_data)
        assert create_response.status_code == 200
        response = delete_pet_by_id(pet_data['id'])
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
        response_get = get_pet_by_id(pet_data['id'])
        assert response_get.status_code == 404, "Pet was not deleted."

    def test_delete_pet_by_id_negative_not_found(self):
        response = delete_pet_by_id(999999999)
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}. Response: {response.text}"

    def test_get_pet_by_id_positive(self):
        create_response = create_pet(pet_data)
        assert create_response.status_code == 200
        response = get_pet_by_id(pet_data['id'])
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
        retrieved_pet = response.json()
        assert retrieved_pet['id'] == pet_data['id'], "Retrieved pet ID does not match."
        assert retrieved_pet['name'] == pet_data['name']
        delete_pet_by_id(pet_data['id'])

    def test_get_pet_by_id_negative_not_found(self):
        response = get_pet_by_id(random())
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}. Response: {response.text}"


    def test_update_pet_positive(self):
        create_response = create_pet(pet_data)
        assert create_response.status_code == 200
        updated_pet_data = pet_data.copy()
        updated_pet_data['name'] = "Charlie"
        updated_pet_data['status'] = "sold"
        response = update_pet(updated_pet_data)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
        response_get = get_pet_by_id(updated_pet_data['id'])
        assert response_get.status_code == 200
        updated_pet_from_get = response_get.json()
        assert updated_pet_from_get['name'] == "Charlie", "Name was not updated."
        assert updated_pet_from_get['status'] == "sold", "Status was not updated"
        delete_pet_by_id(updated_pet_from_get['id'])

    def test_update_pet_negative_not_found(self):
        response = update_pet(None)
        assert response.status_code == 405, f"Expected status code 405, got {response.status_code}. Response: {response.text}"



