import allure
from config.constants import BASE_URL

class UserActions:
    @staticmethod
    def get_user_data(auth_session):
        with allure.step("Получение айди пользователя"):
            user_data_response = auth_session.get(f"{BASE_URL}/api/v1/users/me")
            return user_data_response

    @staticmethod
    def delete_account(auth_session):
        with allure.step("Удаление пользователя"):
            response = auth_session.delete(f"{BASE_URL}/api/v1/users/me")
            return response
