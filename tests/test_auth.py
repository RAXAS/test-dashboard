import allure

from config.constants import BASE_URL
from config.items_utils import ItemActions
from config.user_utils import UserActions


@allure.feature("Тесты для работы с юзером")
class TestAuth:
    @allure.story("Тест создания пользователя")
    def test_registration_new_user(self, auth_session):
        UserActions.get_user_id(auth_session)
        UserActions.delete_account(auth_session)

    @allure.story("Проверка что пользователь может получить закрытую информацию")
    def test_auth_user_can_get_created_items(self, auth_session, item_data):
        ItemActions.create_item(auth_session, item_data)
        ItemActions.get_user_items_list(auth_session)
        UserActions.delete_account(auth_session)
