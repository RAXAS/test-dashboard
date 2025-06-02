import pytest
import requests
import random
import string
from faker import Faker

from config.constants import AUTH_HEADERS, BASE_URL, ITEMS_HEADERS
from config.models.item_model import ItemCreate, RandomId
from config.models.user_model import UserCreds, UserBase, UserToken
from config.user_utils import UserActions

fake = Faker()

@pytest.fixture(scope="function")
def user_credentials() -> UserCreds:
    user_body = UserCreds(
        email=fake.email(),
        password=fake.password(),
        full_name=fake.name()
    )
    return user_body

@pytest.fixture(scope="function")
def generate_random_email_max_length(length=64):
    characters = string.ascii_letters
    random_email = ''.join(random.choice(characters) for _ in range(length)) + "@gmail.com"
    return random_email

@pytest.fixture(scope="function")
def generate_random_password_max_length(length=40):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(random.choice(characters) for _ in range(length))
    return random_password

@pytest.fixture(scope="function")
def register_user(user_credentials):
    response = UserActions.create_user(user_credentials)
    return response

@pytest.fixture(scope="function")
def user_login(user_credentials, register_user) -> UserToken:
    login_body = UserBase(
        username=user_credentials.email,
        password=user_credentials.password
    )
    body = UserActions.login_user(login_body)
    response_body = UserToken.model_validate_json(body.text)
    return response_body

@pytest.fixture(scope="function")
def auth_session(user_login):
    body = UserActions.user_session(user_login.access_token)
    return body

@pytest.fixture(scope="function")
def session_without_auth():
    session = requests.Session()
    session.headers.update(AUTH_HEADERS)
    return session

@pytest.fixture(scope="function")
def item_data() -> ItemCreate:
    return ItemCreate(
        title=fake.word().capitalize(),
        description=fake.sentence(nb_words=10)
    )

@pytest.fixture(scope="function")
def update_item_data() -> ItemCreate:
    return ItemCreate(
        title=fake.word().capitalize(),
        description=fake.sentence(nb_words=10)
    )

@pytest.fixture(scope="function")
def random_uuid() -> RandomId:
    return RandomId(
        id=fake.uuid4()
    )
