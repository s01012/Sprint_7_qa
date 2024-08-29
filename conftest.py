import pytest
import random
from datetime import datetime


@pytest.fixture
def default_user():
    dict_authorization = {'login': 'Ke$ha',
                          'password': 'qwe123',
                          'firstName': 'Иннокентий'}
    return dict_authorization

@pytest.fixture
def generator():
    alphabet = [chr(i) for i in range(97, 123)]

    dict_registration = {
        'login': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}'),
        'password': random.randint(100000, 999999),
        'first_name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
    }
    return dict_registration

@pytest.fixture
def generator_order():
    russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    dict_order = {
        'first_name': (''.join(random.choices(russian_alphabet, k=5)) + f'_тест_имя'),
        'last_name': (''.join(random.choices(russian_alphabet, k=5)) + f'_тест_фамилия'),
        'address': f'ул.' + (''.join(random.choices(russian_alphabet, k=5)) + f'_тестовый_адрес' + f' ' + f'д.{random.randint(10, 99)}'),
        'metro_station': random.randint(1, 9),
        'phone': f'+7{random.randint(1000000000, 9999999999)}',
        'rent_time': random.randint(1, 6),
        'delivery_date': datetime.now().strftime('%Y-%m-%d'),
        'comment': 'Один человек, один самокат - НЕТ петушарингу',
        'color': ''
    }
    return dict_order