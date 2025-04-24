import allure
from config.constants import BASE_URL

class ItemActions:
    @staticmethod
    def create_item(auth_session, item_data):
        with allure.step("Создание нового айтема"):
            response = auth_session.post(f"{BASE_URL}/api/v1/items/", json=item_data)
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 200, "Creation Error"
            return response.json()

    @staticmethod
    def get_item_by_id(auth_session, item_id):
        with allure.step("Получение айтема по айди"):
            response = auth_session.get(f"{BASE_URL}/api/v1/items/{item_id}")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 200, f"Error get item with id {item_id}"
            return response.json()

    @staticmethod
    def get_user_items_list(auth_session):
        with allure.step("Получение списка айтемов юзера"):
            response = auth_session.get(f"{BASE_URL}/api/v1/items/")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 200, "Error get items list"
            return response.json()

    @staticmethod
    def delete_item(auth_session, item_id):
        with allure.step("Удаление айтема"):
            response = auth_session.delete(f"{BASE_URL}/api/v1/items/{item_id}")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 200, "Error delete item"

    @staticmethod
    def update_item(auth_session, item_id, update_item_data):
        with allure.step("Обновление айтема"):
            response = auth_session.put(f"{BASE_URL}/api/v1/items/{item_id}", json=update_item_data)
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 200, "Error update item"
            return response.json()

    @staticmethod
    def get_deleted_item_by_id(auth_session, item_id):
        with allure.step("Получение удалённого айтема по айди"):
            response = auth_session.get(f"{BASE_URL}/api/v1/items/{item_id}")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 404, f"Error get item with id {item_id}"
            return response.json()

    @staticmethod
    def create_item_with_mistake_in_title(auth_session, item_data):
        with allure.step("Создание айтема с ошибкой в заголовке"):
            response = auth_session.post(f"{BASE_URL}/api/v1/items/", json=item_data)
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 422, "Item created without title"
            return response.json()

    @staticmethod
    def create_item_without_token(session_without_auth, item_data):
        with allure.step("Создание айтема без токена"):
            response = session_without_auth.post(f"{BASE_URL}/api/v1/items/", json=item_data)
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 401, "Item created without title"
            return response.json()

    @staticmethod
    def get_item_by_id_without_token(session_without_auth, item_id):
        with allure.step("Получение айтема по айди без токена"):
            response = session_without_auth.get(f"{BASE_URL}/api/v1/items/{item_id}")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 401, "Error get user's items"
            assert response.json()["detail"] == 'Not authenticated', "Error are not matched"
            return response.json()

    @staticmethod
    def update_item_without_token(session_without_auth, item_id, update_item_data):
        with allure.step("Обновление айтема без токена"):
            response = session_without_auth.put(f"{BASE_URL}/api/v1/items/{item_id}", json=update_item_data)
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 401, "Error update item"
            return response.json()

    @staticmethod
    def delete_not_existing_item(auth_session, item_id):
        with allure.step("Удаление несуществующего айтема"):
            response = auth_session.delete(f"{BASE_URL}/api/v1/items/{item_id}")
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 404, "Error delete item"

    @staticmethod
    def update_not_existing_item(auth_session, item_id, update_item_data):
        with allure.step("Обновление айтема"):
            response = auth_session.put(f"{BASE_URL}/api/v1/items/{item_id}", json=update_item_data)
            allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
            assert response.status_code == 404, "Error update item"
            return response.json()
