import random
import string


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_random_phone():
    return f"+7 9{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}"


def generate_random_order_data(color=None):
    return {
        "firstName": generate_random_string(),
        "lastName": generate_random_string(),
        "address": generate_random_string(),
        "metroStation": random.randint(1, 10),
        "phone": generate_random_phone(),
        "rentTime": random.randint(1, 10),
        "deliveryDate": "2025-03-25",
        "comment": generate_random_string(),
        "color": color if color else []
    }
