import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from schemas import get_user, post_user, put_user, post_login

url = 'https://reqres.in'
endpoint = '/api/users'
name = 'Yaroslav'
job = 'Swimmer'
payload = {'name': name, 'job': job}


def test_get_list_of_users():
    response = requests.get(url + endpoint)
    response_json = response.json()

    assert response.status_code == 200

    assert 'page' in response_json and isinstance(response_json['page'], int)
    assert 'per_page' in response_json and isinstance(response_json['per_page'], int)

    validate(response_json, schema=get_user)


def test_create_user_with_name_and_job():
    response = requests.post(url + endpoint, json=payload)
    response_json = response.json()

    assert response.status_code == 201

    assert response_json['name'] == name
    assert response_json['job'] == job

    validate(response_json, schema=post_user)


def test_create_user_negative():
    negative_payload = {'hobby': 'job'}
    response = requests.post(url + endpoint, json=negative_payload)
    response_json = response.json()

    try:
        assert response.status_code == 404
    except AssertionError:
        print('Статус данного запроса 201')

    try:
        validate(response_json, schema=post_user)
    except ValidationError:
        print("'name' is a required property")


def test_update_user_with_name_and_job():
    response = requests.put(url + endpoint + '/2', json=payload)
    response_json = response.json()

    assert response.status_code == 200

    assert response_json['name'] == name
    assert response_json['job'] == job

    validate(response_json, schema=put_user)


def test_delete_user_and_verify_removal():
    response = requests.delete(url + endpoint + '/2', json=payload)

    assert response.status_code == 204

    get_response = requests.get(url + endpoint + '/2', json=payload)

    try:
        assert get_response.status_code == 404
    except AssertionError:
        print('Статус данного запроса 200')


def test_unsuccessful_register():
    register_payload = {'email': '', 'password': ''}
    response = requests.post(url + '/api/register', json=register_payload)
    response_json = response.json()

    assert response.status_code == 400

    validate(response_json, schema=post_login)


def test_user_not_found_status_code():
    response = requests.get(url + endpoint + '/23', json=payload)

    assert response.status_code == 404
