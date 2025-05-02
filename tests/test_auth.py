import allure

from config.items_utils import ItemActions
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
        register_user_response = register_user
        assert register_user_response.json()["email"] == user_credentials["email"], "Emails are not matched"
        assert register_user_response.json()["is_active"] == True, "User is not active"
        assert register_user_response.json()["is_superuser"] == False, "User is superuser"
        assert register_user_response.json()["full_name"] == user_credentials["full_name"], "full_name are not matched"
        assert register_user_response.json()["id"] != "" or None, "ID is not exist"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка авторизации пользователя")
    def test_login_user(self, user_login, auth_session):
        login_user_response = user_login
        assert login_user_response.status_code == 200, "Error create user"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"


    @allure.story("Проверка получения токена пользователя")
    def test_get_user_access_token(self, user_login, auth_session):
        user_token_response = user_login
        assert user_token_response.status_code == 200, "Error create user"
        assert "access_token" in user_token_response.json(), "access_token is missing in the response"
        assert "access_token" is not "" or None
        assert user_token_response.json()["token_type"] == "bearer", "Error token_type"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка получения данных пользователя после авторизации")
    def test_user_authorization(self, auth_session, user_credentials):
        user_data_response = UserActions.get_user_data(auth_session)
        assert user_data_response.status_code == 200, "Error authorization user"
        assert user_data_response.json()["email"] == user_credentials["email"], "Emails are not matched"
        assert user_data_response.json()["is_active"] == True, "User is not active"
        assert user_data_response.json()["is_superuser"] == False, "User is superuser"
        assert user_data_response.json()["full_name"] == user_credentials["full_name"], "full_name are not matched"
        assert user_data_response.json()["id"] != "" or None, "ID is not exist"
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
        user_credentials["email"] = generate_random_email_max_length
        register_user_response = UserActions.create_user(user_credentials)
        assert register_user_response.status_code == 200, "Error create user"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка регистрации пользователя с превышением количества символов в email")
    def test_register_with_too_many_symbols_in_email(self, user_credentials, generate_random_email_max_length, register_user, auth_session):
        user_credentials["email"] = "i" + generate_random_email_max_length
        register_user_response = UserActions.create_user(user_credentials)
        assert register_user_response.status_code == 422, "Wrong status code"
        assert register_user_response.json()['detail'][0]['msg'] == "value is not a valid email address: The email address is too long before the @-sign (1 character too many).", "Wrong error"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"

    @allure.story("Проверка регистрации пользователя со спецсимволами в email")
    def test_register_with_wrong_symbols_in_email(self, user_credentials, register_user, auth_session):
        user_credentials["email"] = "sfndl#%jkfuig;ngvj$%kzdngkjlv,#@%dfbdfb%45cfbgbf^@#@gmail.com"
        register_user_response = UserActions.create_user(user_credentials)
        assert register_user_response.status_code == 422, "User created"

    @allure.story("Проверка регистрации пользователя с невалидным email")
    def test_registration_fails_with_invalid_email(self, user_credentials, generate_random_email_max_length, register_user):
        user_credentials["email"] = "fdhdsgjkdgsnjnjdsfllsfd"
        register_user_response = UserActions.create_user(user_credentials)
        print(register_user_response.json())
        assert register_user_response.status_code == 422, "User created"
        assert register_user_response.json()['detail'][0]['msg'] == "value is not a valid email address: An email address must have an @-sign.", "Wrong error"

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
        user_credentials["password"] = generate_random_password_max_length
        register_user_response = UserActions.create_user(user_credentials)
        assert register_user_response.status_code == 200, "Error create user"
        deleted_account_response = UserActions.delete_account(auth_session)
        assert deleted_account_response.status_code == 200, "Error delete account"





# ✅ Чек-лист проверок регистрации
# 📌 Позитивные сценарии:
#  Успешная регистрация с валидными данными (email, password, full_name). ✅
#
#  Регистрация с максимальной длиной полей.
#
#  Регистрация с минимальной длиной полей (например, минимальный пароль).
#
# 📌 Негативные сценарии:
#  Регистрация с уже существующим email.
#
#  Регистрация с невалидным email.
#
#  Регистрация с пустым паролем.
#
#  Регистрация с недостаточной длиной пароля.
#
#  Регистрация с пустым email или full_name.
#
#  Регистрация с невалидным форматом полей (спецсимволы, пробелы).
#
# 📌 Проверки ответов API:
#  Статус-код при успешной регистрации (200 или 201). ✅
#
#  Корректный ответ при ошибке (правильный статус-код и информативный текст ошибки).
#
# ✅ Чек-лист проверок авторизации
# 📌 Позитивные сценарии:
#  Успешная авторизация после регистрации.
#
#  Получение корректного JWT токена.
#
#  Повторная авторизация с уже зарегистрированными данными.
#
# 📌 Негативные сценарии:
#  Авторизация с неверным паролем.
#
#  Авторизация с несуществующим email.
#
#  Авторизация с пустыми полями.
#
#  Авторизация с невалидным форматом email.
#
# 📌 Проверки токенов:
#  Корректный формат и структура токена (JWT).
#
#  Попытка использования невалидного или устаревшего токена.
#
#  Попытка использования токена без авторизации в заголовках (доступ должен быть запрещён).
#
# ✅ Чек-лист проверок сессий (с авторизацией и без)
#  Доступ к защищенным ресурсам с корректным токеном.
#
#  Доступ к защищенным ресурсам без токена (должен быть запрещён).
#
#  Доступ с невалидным токеном (должен быть запрещён).
#
#  Проверка корректности заголовков запроса (AUTH_HEADERS, ITEMS_HEADERS).
#
# ✅ Проверка данных пользователя
#  Проверка сохранения данных пользователя после регистрации.
#
#  Проверка получения информации пользователя после авторизации.
#
#  Проверка возможности обновления пользовательских данных.
#
# 🚩 Дополнительные проверки (опционально, но рекомендуется)
#  Проверка времени ответа API при регистрации и авторизации (для оценки производительности).
#
#  Проверка обработки большого количества регистраций или логинов (нагрузочное тестирование).
#
#  Проверка безопасности: попытки SQL-инъекций и других атак на поля формы.