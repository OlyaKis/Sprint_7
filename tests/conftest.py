import pytest
import allure
import requests
from utils.api_client import delete_courier, login_courier
from utils.constants import COURIER_ENDPOINT, STATUS_CREATED, STATUS_OK
from utils.data_generator import generate_random_string


@pytest.fixture
def courier():
    with allure.step("Создание нового курьера"):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(COURIER_ENDPOINT, json=payload)

        if response.status_code != STATUS_CREATED:
            pytest.fail(f"Ошибка при создании курьера: {response.status_code}, {response.text}")

    with allure.step("Авторизация созданного курьера"):
        login_response = login_courier(login, password)
        if login_response.status_code != STATUS_OK:
            pytest.fail(f"Ошибка при авторизации курьера: {login_response.status_code}, {login_response.text}")

    courier_id = login_response.json().get("id")

    if not courier_id:
        pytest.fail("Ошибка: не получен courier_id после авторизации!")

    yield login, password, courier_id

    with allure.step("Удаление созданного курьера после теста"):
        delete_response = delete_courier(courier_id)

        if delete_response.status_code != STATUS_OK:
            pytest.fail(f"Ошибка при удалении курьера: {delete_response.status_code}, {delete_response.text}")


@pytest.fixture
def create_order_data():
    return [["BLACK"], ["GREY"], ["BLACK", "GREY"], []]
