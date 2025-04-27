import allure
from tests.conftest import auth_session, item_data, update_item_data, session_without_auth
from config.items_utils import ItemActions
from config.user_utils import UserActions

@allure.feature("Тесты для работы с айтемами")
class TestItems:
    @allure.story("Тест создания айтема")
    def test_create_item_with_valid_data(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        item_id = created_item.json()["id"]
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"
        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body.status_code == 200, f"Error get item by ID: {item_id}"
        assert get_response_body.json()["title"] == item_data["title"], "Titles aren't matched"
        assert get_response_body.json()["description"] == item_data["description"], "Description aren't matched"
        assert get_response_body.json()["owner_id"] == user_data.json()["id"], "Owner ids' aren't matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест тела ответа при создании айтема")
    def test_response_body_of_created_item(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"
        assert created_item.json()["title"] == item_data["title"], "Titles are not matched"
        assert created_item.json()["description"] == item_data["description"], "Description are not matched"
        assert created_item.json()["owner_id"] == user_data.json()["id"]
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест созданный айтем отображается в списке всех айтемов")
    def test_created_item_appears_in_list_items(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        item_id = created_item.json()["id"]
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"

        user_items_list_response = ItemActions.get_user_items_list(auth_session)
        assert user_items_list_response.status_code == 200, "Error get items list"
        items_data = user_items_list_response.json()["data"]
        items_by_id = {item["id"]: item for item in items_data}
        assert item_id in items_by_id, "Items ids' aren't matched"
        created_item_response = items_by_id[item_id]
        assert created_item_response["title"] == item_data["title"], "Titles aren't matched"
        assert created_item_response["description"] == item_data["description"], "Description aren't matched"
        assert created_item_response["owner_id"] == user_data.json()["id"], "Owner ids' aren't matched"
        assert user_items_list_response.json()["count"] == 1, "Counts aren't matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест созданный айтем отображается при переходу по его ID в URL")
    def test_get_created_item_by_id(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        item_id = created_item.json()["id"]
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"

        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body.status_code == 200, f"Error get item by ID: {item_id}"
        assert get_response_body.json()["title"] == item_data["title"], "Titles aren't matched"
        assert get_response_body.json()["description"] == item_data["description"], "Description aren't matched"
        assert get_response_body.json()["owner_id"] == user_data.json()["id"], "Owner ids' aren't matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест обновления созданного айтема")
    def test_update_created_item(self, auth_session, item_data, update_item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        item_id = created_item.json()["id"]
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"
        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body.status_code == 200, f"Error get item by ID: {item_id}"

        updated_item_response = ItemActions.update_item(auth_session, item_id, update_item_data)
        assert updated_item_response.status_code == 200, "Error update item"
        assert updated_item_response.json()["title"] == update_item_data["title"], "Titles aren't matched"
        assert updated_item_response.json()["description"] == update_item_data["description"], "Description aren't matched"
        assert updated_item_response.json()["owner_id"] == user_data.json()["id"], "Owner ids' aren't matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест удаления созданного айтема")
    def test_delete_created_item(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        item_id = created_item.json()["id"]
        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body.status_code == 200, f"Error get item by ID: {item_id}"
        deleted_item_response = ItemActions.delete_item(auth_session, item_id)
        assert deleted_item_response.status_code == 200, "Error delete item"
        get_deleted_item_response = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_deleted_item_response.status_code == 404, f"Error - item isn't deleted, ID: {item_id}"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест создания айтема без заголовка")
    def test_create_item_with_empty_title(self, auth_session):
        item_data = {
            "title": "",
            "description": "A lot of words"
        }
        error_create_response = ItemActions.create_item(auth_session, item_data)
        assert error_create_response.status_code == 422, "Item created without title"
        assert error_create_response.json()['detail'][0]['msg'] == "String should have at least 1 character", "Error are not matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест создания айтема с пустым описанием")
    def test_create_item_with_empty_description(self, auth_session):
        item_data = {
            "title": "A lot of words",
            "description": ""
        }
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест создания айтема с None в заголовке")
    def test_create_item_with_none_in_title(self, auth_session):
        item_data = {
            "title": None,
            "description": "A lot of words"
        }
        error_create_response = ItemActions.create_item(auth_session, item_data)
        assert error_create_response .json()['detail'][0]['msg'] == "Input should be a valid string", "Error are not matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест создания айтема с None в описании")
    def test_create_item_with_none_in_description(self, auth_session):
        item_data = {
            "title": "A lot of words",
            "description": None
        }
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест создания айтема без токена")
    def test_create_item_without_token(self, session_without_auth, item_data):
        error_create_response = ItemActions.create_item(session_without_auth, item_data)
        assert error_create_response.status_code == 401, "Error. Item Created"

    @allure.story("Негативный тест получения созданного айтема без токена")
    def test_get_created_item_without_token(self, auth_session, item_data, session_without_auth):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        item_id = created_item.json()["id"]
        error_get_item_response = ItemActions.get_item_by_id(session_without_auth, item_id)
        assert error_get_item_response.status_code == 401, f"Error, item found without token"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест обновления созданного айтема без токена")
    def test_update_created_item_without_token(self, auth_session, item_data, update_item_data, session_without_auth):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        item_id = created_item.json()["id"]
        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body.status_code == 200, f"Error get item by ID: {item_id}"
        error_updated_item_response = ItemActions.update_item(session_without_auth, item_id, update_item_data)
        assert error_updated_item_response.status_code == 401, "Error update item"
        assert error_updated_item_response.json()["detail"] == 'Not authenticated', "Error are not matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест удаления созданного айтема дважды")
    def test_delete_one_item_twice(self, auth_session, item_data):
        error_create_response = ItemActions.create_item(auth_session, item_data)
        assert error_create_response.status_code == 200, "Creation Error"
        item_id = error_create_response.json()["id"]
        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body.status_code == 200, f"Error get item by ID: {item_id}"
        deleted_item_response = ItemActions.delete_item(auth_session, item_id)
        assert deleted_item_response.status_code == 200, "Error delete item"
        second_delete_item_response = ItemActions.delete_item(auth_session, item_id)
        assert second_delete_item_response.status_code == 404, "Error delete item"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест удаления несуществующего айтема")
    def test_delete_not_existent_item(self, auth_session):
        item_id = "511172a0-45df-4945-99af-8821d8bbd2bf"
        delete_not_existent__item_response = ItemActions.delete_item(auth_session, item_id)
        assert delete_not_existent__item_response.status_code == 404, "Error delete item"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест обновления несуществующего айтема")
    def test_update_non_existent_item(self, auth_session, item_data):
        item_id = "511172a0-45df-4945-99af-8821d8bbd2bf"
        error_updated_item_response = ItemActions.update_item(auth_session, item_id, item_data)
        assert error_updated_item_response.status_code == 404, "Error, not existing item was updated"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест создания двадцати айтемов")
    def test_create_twenty_items(self, auth_session):
        for i in range(20):
            item_data = {
                "title": f"Test Item {i}",
                "description": f"Test Description {i}"
            }
            created_item = ItemActions.create_item(auth_session, item_data)
            assert created_item.status_code == 200, "Creation Error"
        user_items_list_response = ItemActions.get_user_items_list(auth_session)
        assert user_items_list_response.status_code == 200, "Error get items list"
        assert user_items_list_response.json()["count"] == 20, "Created items aren't 20"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"
