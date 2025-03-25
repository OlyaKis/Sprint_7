import pytest
import requests
import allure
from utils.api_client import register_new_courier_and_return_login_password, login_courier
from utils.data_generator import generate_random_string
from utils.constants import COURIER_ENDPOINT, STATUS_CREATED, STATUS_CONFLICT, STATUS_NOT_FOUND, STATUS_OK


@pytest.fixture
def courier():
    response, login, password = register_new_courier_and_return_login_password()
    if response.status_code != STATUS_CREATED:
        pytest.fail(f"Не удалось создать курьера, ошибка {response.status_code}")
    return login, password


@allure.feature('Couriers')
class TestCreateCourier:
    @allure.story('Creating new courier')
    def test_create_courier(self):
        response, login, password = register_new_courier_and_return_login_password()

        with allure.step('Проверка статуса ответа и успешного создания курьера'):
            assert response.status_code == STATUS_CREATED, f'Ожидали статус {STATUS_CREATED}, получили {response.status_code}'
            assert response.json() == {"ok": True}, f'Ожидали {"ok": True}, получили {response.json()}'

    @allure.story('Creating new duplicate courier')
    def test_create_duplicate_courier(self, courier):
        login, password = courier
        payload = {"login": login, "password": password, "firstName": generate_random_string()}

        with allure.step('Отправка запроса на создание курьера с уже занятым логином'):
            response = requests.post(COURIER_ENDPOINT, json=payload)

        with allure.step('Проверка статуса и текста ошибки для дубликата курьера'):
            assert response.status_code == STATUS_CONFLICT, f'Ожидали статус {STATUS_CONFLICT}, получили {response.status_code}'
            assert "Этот логин уже используется" in response.text, 'Ошибка не совпадает'

    @allure.story('Creating courier missing field')
    def test_create_courier_missing_field(self):
        payload = {"login": generate_random_string(), "password": generate_random_string()}

        with allure.step('Отправка запроса на создание курьера без обязательного поля'):
            response = requests.post(COURIER_ENDPOINT, json=payload)

        with allure.step('Проверка статуса ответа на создание курьера с недостающим полем'):
            assert response.status_code == STATUS_CREATED, f'Ожидали статус {STATUS_CREATED}, получили {response.status_code}'


@allure.feature('Couriers')
class TestLoginCourier:
    @allure.story('Success courier login')
    def test_login_courier_success(self, courier):
        login, password = courier
        response = login_courier(login, password)

        with allure.step('Проверка успешного входа курьера'):
            assert response.status_code == STATUS_OK, f'Ожидали статус {STATUS_OK}, получили {response.status_code}'
            assert "id" in response.json(), 'Отсутствует "id" в ответе'

    @allure.story('Login courier with wrong password')
    def test_login_courier_wrong_password(self):
        login = generate_random_string()
        password = generate_random_string()
        register_new_courier_and_return_login_password()

        with allure.step('Отправка запроса на вход с неверным паролем'):
            response = login_courier(login, "wrongpassword")

        with allure.step('Проверка статуса и текста ошибки при неверном пароле'):
            assert response.status_code == STATUS_NOT_FOUND, f'Ожидали статус {STATUS_NOT_FOUND}, получили {response.status_code}'
            assert "Учетная запись не найдена" in response.text, 'Ошибка не совпадает'

    @allure.story('Login courier with missing field')
    def test_login_courier_missing_field(self):
        payload = {"login": generate_random_string()}

        with allure.step('Отправка запроса на вход без обязательного поля'):
            response = requests.post(COURIER_ENDPOINT + "/login", json=payload)

        with allure.step('Проверка статуса ответа при недостаточности данных'):
            assert response.status_code == 504, f'Ожидали статус 504, получили {response.status_code}'
            print(response.text)
