import allure
import requests
from requests import session

from config.constants import BASE_URL, AUTH_HEADERS, ITEMS_HEADERS


class UserActions:
    @staticmethod
    def create_user(register_body):
        with allure.step("Создание пользователя"):
            register_user_response = requests.post(f"{BASE_URL}/api/v1/users/signup/", json=register_body.dict())
            return register_user_response

    @staticmethod
    def login_user(login_body):
        with allure.step("Авторизация пользователя"):
            login_user_response = requests.post(f"{BASE_URL}/api/v1/login/access-token/", data=login_body.dict())
            return login_user_response

    @staticmethod
    def user_session(token):
        session_user = requests.Session()
        session_user.headers.update(AUTH_HEADERS)
        session_user.headers.update(ITEMS_HEADERS)
        session_user.headers.update({"Authorization": f"Bearer {token}"})
        return session_user

    @staticmethod
    def get_user_data(auth_session):
        with allure.step("Получение данных пользователя"):
            user_data_response = auth_session.get(f"{BASE_URL}/api/v1/users/me")
            return user_data_response

    @staticmethod
    def delete_account(auth_session):
        with allure.step("Удаление пользователя"):
            response = auth_session.delete(f"{BASE_URL}/api/v1/users/me")
            return response
