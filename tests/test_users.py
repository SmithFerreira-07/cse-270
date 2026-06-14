import requests


def test_users_valid_credentials():
    response = requests.get("http://127.0.0.1:8000/users/?username=admin&password=qwerty")
    assert response.status_code == 200


def test_users_invalid_credentials():
    response = requests.get("http://127.0.0.1:8000/users/?username=admin&password=admin")
    assert response.status_code == 401

