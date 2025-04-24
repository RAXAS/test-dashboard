import allure
from config.constants import BASE_URL

class UserActions:
    @staticmethod
    def get_user_id(auth_session):
        with allure.step("Получение айди пользователя"):
            user_data = auth_session.get(f"{BASE_URL}/api/v1/users/me")
            assert user_data.status_code == 200, "Error get user's data"
            return user_data.json()["id"]

    @staticmethod
    def delete_account(auth_session):
        with allure.step("Удаление пользователя"):
            response = auth_session.delete(f"{BASE_URL}/api/v1/users/me")
            assert response.status_code == 200, "Error delete account"
