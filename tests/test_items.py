import allure
from tests.conftest import auth_session, item_data, update_item_data, session_without_auth
from config.items_utils import ItemActions
from config.user_utils import UserActions
from config.models.item_model import BaseItem, ItemsPage, ItemCreate, ValidationErrorItemResponse
from config.models.user_model import GetUser, ErrorUserResponse


@allure.feature("Тесты для работы с айтемами")
class TestItems:
    @allure.story("Тест создания айтема")
    def test_create_item_with_valid_data(self, auth_session, item_data):

        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)
        assert created_item_response.title == item_data.title
        assert created_item_response.description == item_data.description

        user_credentials_response = UserActions.get_user_data(auth_session)
        assert user_credentials_response.status_code == 200, "Error get user's data"
        user = GetUser.model_validate_json(user_credentials_response.text)

        get_created_item = ItemActions.get_item_by_id(auth_session, created_item_response.id)
        assert get_created_item.status_code == 200, f"Error get item by ID: {created_item_response.id}"
        get_created_item_body = BaseItem.model_validate_json(get_created_item.text)
        assert get_created_item_body.title == item_data.title, "Titles aren't matched"
        assert get_created_item_body.description == item_data.description, "Description aren't matched"
        assert get_created_item_body.owner_id == user.id, "Owner ids' aren't matched"

        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест тела ответа при создании айтема")
    def test_response_body_of_created_item(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)

        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"
        user_data_response = GetUser.model_validate_json(user_data.text)

        assert created_item_response.title == item_data.title, "Titles are not matched"
        assert created_item_response.description == item_data.description, "Description are not matched"
        assert created_item_response.owner_id == user_data_response.id

        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест созданный айтем отображается в списке всех айтемов") # Тут не готово
    def test_created_item_appears_in_list_items(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)

        item_id = created_item_response.id
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"
        user_data_response = GetUser.model_validate_json(user_data.text)

        user_items_list = ItemActions.get_user_items_list(auth_session)
        assert user_items_list.status_code == 200, "Error get items list"
        user_items_list_response = ItemsPage.model_validate_json(user_items_list.text)

        items_data = user_items_list_response.data
        items_by_id = {item.id: item for item in items_data}
        assert item_id in items_by_id, "Items ids' aren't matched"
        created_item_response = items_by_id[item_id]
        assert created_item_response.title == item_data.title, "Titles aren't matched"
        assert created_item_response.description == item_data.description, "Description aren't matched"
        assert created_item_response.owner_id == user_data_response.id, "Owner ids' aren't matched"
        assert user_items_list.json()["count"] == 1, "Counts aren't matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест созданный айтем отображается при переходу по его ID в URL")
    def test_get_created_item_by_id(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)

        item_id = created_item_response.id
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"
        user_data_response = GetUser.model_validate_json(user_data.text)

        item_by_id = ItemActions.get_item_by_id(auth_session, item_id)
        assert item_by_id.status_code == 200, f"Error get item by ID: {item_id}"
        item_by_id_response = BaseItem.model_validate_json(item_by_id.text)

        assert item_by_id_response.title == item_data.title, "Titles aren't matched"
        assert item_by_id_response.description == item_data.description, "Description aren't matched"
        assert item_by_id_response.owner_id == user_data_response.id, "Owner ids' aren't matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест обновления созданного айтема")
    def test_update_created_item(self, auth_session, item_data, update_item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)
        item_id = created_item_response.id
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error get user's data"
        user_data_response = GetUser.model_validate_json(user_data.text)
        item_by_id = ItemActions.get_item_by_id(auth_session, item_id)
        assert item_by_id.status_code == 200, f"Error get item by ID: {item_id}"

        updated_item = ItemActions.update_item(auth_session, item_id, update_item_data)
        assert updated_item.status_code == 200, "Error update item"
        updated_item_response = BaseItem.model_validate_json(updated_item.text)
        assert updated_item_response.title == update_item_data.title, "Titles aren't matched"
        assert updated_item_response.description == update_item_data.description, "Description aren't matched"
        assert updated_item_response.owner_id == user_data_response.id, "Owner ids' aren't matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест удаления созданного айтема")
    def test_delete_created_item(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)
        item_id = created_item_response.id
        item_by_id = ItemActions.get_item_by_id(auth_session, item_id)
        assert item_by_id.status_code == 200, f"Error get item by ID: {item_id}"

        deleted_item_response = ItemActions.delete_item(auth_session, item_id)
        assert deleted_item_response.status_code == 200, "Error delete item"
        deleted_item_by_id = ItemActions.get_item_by_id(auth_session, item_id)
        assert deleted_item_by_id.status_code == 404, f"Error - item isn't deleted, ID: {item_id}"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест создания айтема без заголовка")
    def test_create_item_with_empty_title(self, auth_session):
        item_data = ItemCreate(
            title="",
            description="A lot of words"
        )
        create_item_with_error = ItemActions.create_item(auth_session, item_data)
        assert create_item_with_error.status_code == 422, "Item created without title"
        create_with_error_response = ValidationErrorItemResponse(**create_item_with_error.json())
        assert create_with_error_response.detail[0].msg == "String should have at least 1 character", "Error are not matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест создания айтема с пустым описанием")
    def test_create_item_with_empty_description(self, auth_session):
        item_data = ItemCreate(
            title="A lot of words",
            description=""
    )
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
        created_item_response = BaseItem.model_validate_json(created_item.text)
        item_id = created_item_response.id
        error_get_item_response = ItemActions.get_item_by_id(session_without_auth, item_id)
        assert error_get_item_response.status_code == 401, f"Error, item found without token"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест обновления созданного айтема без токена")
    def test_update_created_item_without_token(self, auth_session, item_data, update_item_data, session_without_auth):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)
        item_id = created_item_response.id
        item_by_id = ItemActions.get_item_by_id(auth_session, item_id)
        assert item_by_id.status_code == 200, f"Error get item by ID: {item_id}"
        error_updated_item = ItemActions.update_item(session_without_auth, item_id, update_item_data)
        assert error_updated_item.status_code == 401, "Error update item"
        error_updated_item_response = ErrorUserResponse(**error_updated_item.json())
        assert error_updated_item_response.detail == 'Not authenticated', "Error are not matched"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест удаления созданного айтема дважды")
    def test_delete_one_item_twice(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        created_item_response = BaseItem.model_validate_json(created_item.text)
        item_id = created_item_response.id
        item_by_id = ItemActions.get_item_by_id(auth_session, item_id)
        assert item_by_id.status_code == 200, f"Error get item by ID: {item_id}"
        deleted_item_response = ItemActions.delete_item(auth_session, item_id)
        assert deleted_item_response.status_code == 200, "Error delete item"
        second_delete_item_response = ItemActions.delete_item(auth_session, item_id)
        assert second_delete_item_response.status_code == 404, "Error delete item"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест удаления несуществующего айтема")
    def test_delete_not_existent_item(self, auth_session, random_uuid):
        item_id = random_uuid
        delete_not_existent__item_response = ItemActions.delete_item(auth_session, item_id)
        assert delete_not_existent__item_response.status_code == 422, "Error delete item"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Негативный тест обновления несуществующего айтема")
    def test_update_non_existent_item(self, auth_session, item_data, random_uuid):
        item_id = random_uuid
        error_updated_item_response = ItemActions.update_item(auth_session, item_id, item_data)
        assert error_updated_item_response.status_code == 422, "Error, not existing item was updated"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Тест создания двадцати айтемов")
    def test_create_twenty_items(self, auth_session):
        for i in range(20):
            item_data = ItemCreate(
                title=f"Test Item {i}",
                description=f"Test Description {i}"
            )
            created_item = ItemActions.create_item(auth_session, item_data)
            assert created_item.status_code == 200, "Creation Error"
        user_items_list = ItemActions.get_user_items_list(auth_session)
        assert user_items_list.status_code == 200, "Error get items list"
        user_items_list_response = ItemsPage.model_validate_json(user_items_list.text)
        assert user_items_list_response.count == 20, "Created items aren't 20"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"
