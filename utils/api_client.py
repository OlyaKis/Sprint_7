import requests
import random
import string
from utils.constants import BASE_URL
from utils.constants import COURIER_ENDPOINT


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def register_new_courier_and_return_login_password():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(COURIER_ENDPOINT, json=payload)

    return response, login, password


def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")


def login_courier(login, password):
    payload = {"login": login, "password": password}
    return requests.post(f"{BASE_URL}/courier/login", json=payload)


def create_order(color=None):
    payload = {
        "firstName": generate_random_string(),
        "lastName": generate_random_string(),
        "address": generate_random_string(),
        "metroStation": random.randint(1, 10),
        "phone": "+7 999 999 99 99",
        "rentTime": random.randint(1, 10),
        "deliveryDate": "2025-03-25",
        "comment": generate_random_string(),
        "color": color if color else []
    }
    return requests.post(f"{BASE_URL}/orders", json=payload)


def get_orders():
    return requests.get(f"{BASE_URL}/orders")
