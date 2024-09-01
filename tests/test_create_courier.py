import allure
import random
import requests
from utils.url import *
from utils.endpoint import *


class TestCreateCourier:
    dict_registration = {}

    @classmethod
    def setup_class(cls):
        alphabet = [chr(i) for i in range(97, 123)]
        cls.dict_registration = {
            'login': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}'),
            'password': random.randint(100000, 999999),
            'first_name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
        }

    @allure.title('Отправляем POST запрос на создание курьера с неиспользованными ранее данными')
    def test_create_courier(self):
        payload = {
            'login': self.dict_registration.get('login'),
            'password': self.dict_registration.get('password'),
            'first_name': self.dict_registration.get('first_name')
        }
        correct_response_body = '{"ok":true}'
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert response.text == correct_response_body and response.status_code == 201

    @allure.title('Отправляем POST запрос на создание курьера с данными, которые уже есть в системе')
    def test_create_identical_courier(self):
        payload = {
            'login': self.dict_registration.get('login'),
            'password': self.dict_registration.get('password'),
            'first_name': self.dict_registration.get('first_name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert 'Этот логин уже используется' in response.text and response.status_code == 409

    @allure.title('Отправляем POST запрос на создание курьера без логина')
    def test_create_courier_without_login(self):
        payload = {
            'login': '',
            'password': self.dict_registration.get('password'),
            'first_name': self.dict_registration.get('first_name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert 'Недостаточно данных для создания учетной записи' in response.text and response.status_code == 400

    @allure.title('Отправляем POST запрос на создание курьера без пароля')
    def test_create_courier_without_password(self):
        payload = {
            'login': self.dict_registration.get('login'),
            'password': '',
            'first_name': self.dict_registration.get('first_name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert 'Недостаточно данных для создания учетной записи' in response.text and response.status_code == 400

    @classmethod
    def teardown_class(cls):
        cls.payload = {
            'login': cls.dict_registration.get('login'),
            'password': cls.dict_registration.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=cls.payload)
        r = response.json()
        requests.delete(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}/{r.get('id')}')
