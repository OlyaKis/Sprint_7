import requests
import allure
from utils.api_client import login_courier
from utils.data_generator import generate_random_string
from utils.constants import COURIER_ENDPOINT, STATUS_CONFLICT, STATUS_NOT_FOUND, STATUS_OK


@allure.feature('Couriers')
class TestCreateCourier:
    @allure.story('Creating new courier')
    def test_create_courier(self, courier):
        login, password, courier_id = courier

        with allure.step('Проверка авторизации созданного курьера'):
            response = login_courier(login, password)
            assert response.status_code == STATUS_OK
            assert "id" in response.json(), "Ответ не содержит 'id'"

    @allure.story('Creating new duplicate courier')
    def test_create_duplicate_courier(self, courier):
        login, password, courier_id = courier

        payload = {"login": login, "password": password, "firstName": generate_random_string()}
        response = requests.post(COURIER_ENDPOINT, json=payload)

        assert response.status_code == STATUS_CONFLICT
        assert "Этот логин уже используется" in response.text

    @allure.story('Creating courier missing field')
    def test_create_courier_missing_field(self):
        payload = {"login": generate_random_string(), "password": generate_random_string()}

        with allure.step('Отправка запроса на создание курьера без обязательного поля'):
            response = requests.post(COURIER_ENDPOINT, json=payload)

        with allure.step('Проверка успешного создания курьера без firstName'):
            assert response.status_code == 201, f'Ожидали 201, получили {response.status_code}'
            assert response.json() == {"ok": True}, f'Ожидали {{"ok": True}}, получили {response.json()}'


@allure.feature('Couriers')
class TestLoginCourier:
    @allure.story('Success courier login')
    def test_login_courier_success(self, courier):
        login, password, _ = courier
        response = login_courier(login, password)

        with allure.step('Проверка успешного входа курьера'):
            assert response.status_code == STATUS_OK
            assert "id" in response.json(), 'Отсутствует "id" в ответе'

    @allure.story('Login courier with wrong password')
    def test_login_courier_wrong_password(self, courier):
        login, _, _ = courier
        response = login_courier(login, "wrongpassword")

        with allure.step('Проверка статуса и текста ошибки при неверном пароле'):
            assert response.status_code == STATUS_NOT_FOUND
            assert "Учетная запись не найдена" in response.text, 'Ошибка не совпадает'

    @allure.story('Login courier with missing field')
    def test_login_courier_missing_field(self):
        payload = {"login": generate_random_string()}

        with allure.step('Отправка запроса на вход без обязательного поля'):
            response = requests.post(COURIER_ENDPOINT + "/login", json=payload)

        with allure.step('Проверка статуса ответа при недостаточности данных'):
            assert response.status_code == 504
            print(response.text)
