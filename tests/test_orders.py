import pytest
import allure
from utils.api_client import create_order, get_orders
from utils.constants import STATUS_CREATED, STATUS_OK


@allure.feature('Orders')
class TestCreateOrder:
    @allure.story('Creating new order')
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order(self, color):

        with allure.step(f'Отправка запроса на создание заказа с цветом: {color}'):
            response = create_order(color)

        with allure.step('Проверка статуса ответа и наличия трека в ответе'):
            assert response.status_code == STATUS_CREATED, f'Ожидали статус {STATUS_CREATED}, получили {response.status_code}'
            assert "track" in response.json(), 'Отсутствует ключ "track" в ответе'


@allure.feature('Orders')
class TestGetOrders:
    @allure.story('Getting order list')
    def test_get_orders(self):

        with allure.step('Отправка запроса на получение всех заказов'):
            response = get_orders()

        with allure.step('Проверка статуса ответа и структуры данных в ответе'):
            assert response.status_code == STATUS_OK, f'Ожидали статус {STATUS_OK}, получили {response.status_code}'
            assert "orders" in response.json(), 'Отсутствует ключ "orders" в ответе'
            assert isinstance(response.json()["orders"], list), 'Данные по заказам должны быть в формате списка'

