import allure
from config.constants import BASE_URL

class ItemActions:
    @staticmethod
    def create_item(auth_session, item_data):
        with allure.step("Создание нового айтема"):
            response = auth_session.post(f"{BASE_URL}/api/v1/items/", json=item_data.dict())
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            return response

    @staticmethod
    def get_item_by_id(auth_session, item_id):
        with allure.step("Получение айтема по айди"):
            response = auth_session.get(f"{BASE_URL}/api/v1/items/{item_id}")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            return response

    @staticmethod
    def get_user_items_list(auth_session):
        with allure.step("Получение списка айтемов юзера"):
            response = auth_session.get(f"{BASE_URL}/api/v1/items/")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            return response

    @staticmethod
    def delete_item(auth_session, item_id):
        with allure.step("Удаление айтема"):
            response = auth_session.delete(f"{BASE_URL}/api/v1/items/{item_id}")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            return response

    @staticmethod
    def update_item(auth_session, item_id, update_item_data):
        with allure.step("Обновление айтема"):
            response = auth_session.put(f"{BASE_URL}/api/v1/items/{item_id}", json=update_item_data.dict())
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            return response
