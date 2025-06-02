import allure

from config.items_utils import ItemActions
from config.models.user_model import GetUser, UserToken, ErrorUserResponse
from config.user_utils import UserActions


@allure.feature("Тесты для работы с юзером")
class TestAuth:
    @allure.story("Проверка регистрации нового пользователя")
    def test_registration_new_user(self, register_user, auth_session):
        register_user_response = register_user
        assert register_user_response.status_code == 200, "Error create user"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка тела ответа при регистрации нового пользователя")
    def test_registration_body_new_user(self, register_user, user_credentials, auth_session, item_data):
        register_user = register_user
        assert register_user.status_code == 200, "Error create user"
        register_user_response = GetUser.model_validate_json(register_user.text)
        assert register_user_response.email == user_credentials.email, "Emails are not matched"
        assert register_user_response.is_active == True, "User is not active"
        assert register_user_response.is_superuser == False, "User is superuser"
        assert register_user_response.full_name == user_credentials.full_name, "full_name are not matched"
        assert register_user_response.id != "" or None, "ID is not exist"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка авторизации пользователя")
    def test_login_user(self, user_login, auth_session):
        assert auth_session is not None
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"


    @allure.story("Проверка получения токена пользователя")
    def test_get_user_access_token(self, user_login, auth_session):
        assert len(user_login.access_token) > 0
        assert user_login.token_type == 'bearer'
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка получения данных пользователя после авторизации")
    def test_user_authorization(self, auth_session, user_credentials):
        user_data = UserActions.get_user_data(auth_session)
        assert user_data.status_code == 200, "Error authorization user"
        user_data_response = GetUser.model_validate_json(user_data.text)
        assert user_data_response.email == user_credentials.email, "Emails are not matched"
        assert user_data_response.is_active == True, "User is not active"
        assert user_data_response.is_superuser == False, "User is superuser"
        assert user_data_response.full_name == user_credentials.full_name, "full_name are not matched"
        assert user_data_response.id != "" or None, "ID is not exist"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка доступа к списку созданных айтемов авторизованного пользователя")
    def test_auth_user_can_get_created_items(self, auth_session, item_data):
        created_item = ItemActions.create_item(auth_session, item_data)
        assert created_item.status_code == 200, "Creation Error"
        user_items_list_response = ItemActions.get_user_items_list(auth_session)
        assert user_items_list_response.status_code == 200, "Error get items list"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка регистрации пользователя с максимальным количеством символов в email")
    def test_register_with_max_length_email(self, user_credentials, generate_random_email_max_length, register_user, auth_session):
        user_credentials.email = generate_random_email_max_length
        register_user_response = UserActions.create_user(user_credentials)
        assert register_user_response.status_code == 200, "Error create user"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка регистрации пользователя с превышением количества символов в email")
    def test_register_with_too_many_symbols_in_email(self, user_credentials, generate_random_email_max_length, register_user, auth_session):
        user_credentials.email = "i" + generate_random_email_max_length
        register_user = UserActions.create_user(user_credentials)
        assert register_user.status_code == 422, "Wrong status code"
        register_user_response = ErrorUserResponse.model_validate_json(register_user.text)
        error_msg = register_user_response.detail[0].msg
        assert "value is not a valid email address" in error_msg, "Wrong error type"
        assert "The email address is too long before the @-sign" in error_msg, "Wrong error reason"
        assert "1 character too many" in error_msg, "Wrong error description"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка регистрации пользователя со спецсимволами в email")
    def test_register_with_wrong_symbols_in_email(self, user_credentials):
        user_credentials.email = "sfndl#%jkfuig;ngvj$%kzdngkjlv,#@%dfbdfb%45cfbgbf^@#@gmail.com"
        register_user_response = UserActions.create_user(user_credentials)
        assert register_user_response.status_code == 422, "User created"

    @allure.story("Проверка регистрации пользователя с невалидным email")
    def test_registration_fails_with_invalid_email(self, user_credentials):
        user_credentials.email = "fdhdsgjkdgsnjnjdsfllsfd"
        register_use_body = UserActions.create_user(user_credentials)
        print(register_use_body.json())
        assert register_use_body.status_code == 422, "User created"
        register_user_response = ErrorUserResponse.model_validate(register_use_body.json())
        assert register_user_response.detail[0].msg == "value is not a valid email address: An email address must have an @-sign.", "Wrong error"

    @allure.story("Регистрация пользователя с теми же данными дважды")
    def test_registration_new_user(self, register_user, user_credentials, auth_session):
        register_first_user_response = register_user
        assert register_first_user_response.status_code == 200, "Error create user"
        register_first_user_response_2 = UserActions.create_user(user_credentials)
        assert register_first_user_response_2.status_code == 400, "User created"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Регистрация пользователя с максимально допустимой длиной пароля")
    def test_register_with_max_length_in_password(self, user_credentials, generate_random_password_max_length, register_user, auth_session):
        user_credentials.email = user_credentials.email + "i"
        user_credentials.password = generate_random_password_max_length
        register_user = UserActions.create_user(user_credentials)
        assert register_user.status_code == 200, "Error create user"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"
