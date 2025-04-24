import allure
from tests.conftest import auth_session, item_data, update_item_data, session_without_auth
from config.items_utils import ItemActions
from config.user_utils import UserActions

@allure.feature("Тесты для работы с айтемами")
class TestItems:
    @allure.story("Тест создания айтема")
    def test_create_item_with_valid_data(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        item_id = created_item["id"]
        owner_id = UserActions.get_user_id(auth_session)
        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body["title"] == item_data["title"], "Titles aren't matched"
        assert get_response_body["description"] == item_data["description"], "Description aren't matched"
        assert get_response_body["owner_id"] == owner_id, "Owner ids' aren't matched"
        UserActions.delete_account(auth_session)

    @allure.story("Тест тела ответа при создании айтема")
    def test_response_body_of_created_item(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        owner_id = UserActions.get_user_id(auth_session)
        assert created_item["title"] == item_data["title"], "Titles are not matched"
        assert created_item["description"] == item_data["description"], "Description are not matched"
        assert created_item["owner_id"] == owner_id
        UserActions.delete_account(auth_session)

    @allure.story("Тест созданный айтем отображается в списке всех айтемов")
    def test_created_item_appears_in_list_items(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        item_id = created_item["id"]
        owner_id = UserActions.get_user_id(auth_session)

        get_response_body = ItemActions.get_user_items_list(auth_session)
        items_data = get_response_body["data"]
        items_by_id = {item["id"]: item for item in items_data}
        assert item_id in items_by_id, "Items ids' aren't matched"
        created_item_response = items_by_id[item_id]
        assert created_item_response["title"] == item_data["title"], "Titles aren't matched"
        assert created_item_response["description"] == item_data["description"], "Description aren't matched"
        assert created_item_response["owner_id"] == owner_id, "Owner ids' aren't matched"
        assert get_response_body["count"] == 1, "Counts aren't matched"
        UserActions.delete_account(auth_session)

    @allure.story("Тест созданный айтем отображается при переходу по его ID в URL")
    def test_get_created_item_by_id(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        item_id = created_item["id"]
        owner_id = UserActions.get_user_id(auth_session)

        get_response_body = ItemActions.get_item_by_id(auth_session, item_id)
        assert get_response_body["title"] == item_data["title"], "Titles aren't matched"
        assert get_response_body["description"] == item_data["description"], "Description aren't matched"
        assert get_response_body["owner_id"] == owner_id, "Owner ids' aren't matched"
        UserActions.delete_account(auth_session)

    @allure.story("Тест обновления созданного айтема")
    def test_update_created_item(self, auth_session, item_data, update_item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        item_id = created_item["id"]
        owner_id = UserActions.get_user_id(auth_session)
        ItemActions.get_item_by_id(auth_session, item_id)

        put_response_body = ItemActions.update_item(auth_session, item_id, update_item_data)
        assert put_response_body["title"] == update_item_data["title"], "Titles aren't matched"
        assert put_response_body["description"] == update_item_data["description"], "Description aren't matched"
        assert put_response_body["owner_id"] == owner_id, "Owner ids' aren't matched"
        UserActions.delete_account(auth_session)

    @allure.story("Тест удаления созданного айтема")
    def test_delete_created_item(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        item_id = created_item["id"]
        ItemActions.get_item_by_id(auth_session, item_id)
        ItemActions.delete_item(auth_session, item_id)
        ItemActions.get_deleted_item_by_id(auth_session, item_id)
        UserActions.delete_account(auth_session)

    @allure.story("Негативный тест создания айтема без заголовка")
    def test_create_item_with_empty_title(self, auth_session):
        item_data = {
            "title": "",
            "description": "A lot of words"
        }
        error_body = ItemActions.create_item_with_mistake_in_title(auth_session, item_data)
        assert error_body['detail'][0]['msg'] == "String should have at least 1 character", "Error are not matched"
        UserActions.delete_account(auth_session)

    @allure.story("Тест создания айтема с пустым описанием")
    def test_create_item_with_empty_description(self, auth_session):
        item_data = {
            "title": "A lot of words",
            "description": ""
        }
        ItemActions.create_item(auth_session, item_data)
        UserActions.delete_account(auth_session)

    @allure.story("Негативный тест создания айтема с None в заголовке")
    def test_create_item_with_none_in_title(self, auth_session):
        item_data = {
            "title": None,
            "description": "A lot of words"
        }
        error_body = ItemActions.create_item_with_mistake_in_title(auth_session, item_data)
        assert error_body['detail'][0]['msg'] == "Input should be a valid string", "Error are not matched"
        UserActions.delete_account(auth_session)

    @allure.story("Тест создания айтема с None в описании")
    def test_create_item_with_none_in_description(self, auth_session):
        item_data = {
            "title": "A lot of words",
            "description": None
        }
        ItemActions.create_item(auth_session, item_data)
        UserActions.delete_account(auth_session)

    @allure.story("Негативный тест создания айтема без токена")
    def test_create_item_without_token(self, session_without_auth, item_data):
        ItemActions.create_item_without_token(session_without_auth, item_data)

    @allure.story("Негативный тест получения созданного айтема без токена")
    def test_get_created_item_without_token(self, auth_session, item_data, session_without_auth):
        created_item = ItemActions.create_item(auth_session, item_data)
        item_id = created_item["id"]
        ItemActions.get_item_by_id_without_token(session_without_auth, item_id)
        UserActions.delete_account(auth_session)

    @allure.story("Негативный тест обновления созданного айтема без токена")
    def test_update_created_item_without_token(self, auth_session, item_data, update_item_data, session_without_auth):
        created_item = ItemActions.create_item(auth_session, item_data)
        item_id = created_item["id"]
        ItemActions.get_item_by_id(auth_session, item_id)
        put_response = ItemActions.update_item_without_token(session_without_auth, item_id, update_item_data)
        assert put_response["detail"] == 'Not authenticated', "Error are not matched"
        UserActions.delete_account(auth_session)

    @allure.story("Негативный тест удаления созданного айтема дважды")
    def test_delete_one_item_twice(self, auth_session, item_data):
        create_response = ItemActions.create_item(auth_session, item_data)
        item_id = create_response["id"]
        ItemActions.get_item_by_id(auth_session, item_id)
        ItemActions.delete_item(auth_session, item_id)
        ItemActions.delete_not_existing_item(auth_session, item_id)
        UserActions.delete_account(auth_session)

    @allure.story("Негативный тест удаления несуществующего айтема")
    def test_delete_non_existent_item(self, auth_session):
        item_id = "511172a0-45df-4945-99af-8821d8bbd2bf"
        ItemActions.delete_not_existing_item(auth_session, item_id)
        UserActions.delete_account(auth_session)

    @allure.story("Негативный тест обновления несуществующего айтема")
    def test_update_non_existent_item(self, auth_session, item_data):
        item_id = "511172a0-45df-4945-99af-8821d8bbd2bf"
        ItemActions.update_not_existing_item(auth_session, item_id, item_data)
        UserActions.delete_account(auth_session)

    @allure.story("Тест создания двадцати айтемов")
    def test_create_twenty_items(self, auth_session):
        for i in range(20):
            item_data = {
                "title": f"Test Item {i}",
                "description": f"Test Description {i}"
            }
            ItemActions.create_item(auth_session, item_data)
        get_user_items = ItemActions.get_user_items_list(auth_session)
        assert get_user_items["count"] == 20, "Created items aren't 20"
        UserActions.delete_account(auth_session)
