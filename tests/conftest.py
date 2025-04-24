import pytest
import requests
from faker import Faker

from config.constants import AUTH_HEADERS, BASE_URL, ITEMS_HEADERS

fake = Faker()


@pytest.fixture(scope="function")
def auth_session():
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)

    email = fake.email()
    password = fake.password()
    full_name = fake.name()
    register_body = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    registration = requests.post(f"{BASE_URL}/api/v1/users/signup/", json=register_body)
    assert registration.status_code == 200, "Creation Error"

    login_body = {
        "username": email,
        "password": password,
    }
    login = requests.post(f"{BASE_URL}/api/v1/login/access-token/", data=login_body)
    assert login.status_code == 200, f"Auth failed: {login.status_code}, {login.text}"
    token = login.json()["access_token"]
    assert token, "No access_token found"
    session.headers.update(ITEMS_HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


@pytest.fixture(scope="function")
def session_without_auth():
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)
    return session

@pytest.fixture(scope="function")
def item_data():
    return {
        "title": fake.word().capitalize(),
        "description": fake.sentence(nb_words=10)
    }

@pytest.fixture(scope="function")
def update_item_data():
    return {
        "title": fake.word().capitalize(),
        "description": fake.sentence(nb_words=10)
    }
