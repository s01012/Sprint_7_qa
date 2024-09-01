import allure
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestAuthorizationCourier:
    dict_registration = {}

    @classmethod
    def setup_class(cls):
        alphabet = [chr(i) for i in range(97, 123)]
        cls.dict_registration = {
            'login': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}'),
            'password': random.randint(100000, 999999),
            'first_name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
        }
        requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=cls.dict_registration)

    @allure.title('Отправляем POST запрос для авторизации ранее зарегистрированного курьера')
    def test_authorization_courier(self):
        payload = {
            'login': self.dict_registration.get('login'),
            'password': self.dict_registration.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert 'id' in response.text and response.status_code == 200

    @allure.title('Отправляем POST запрос для авторизации курьера с несуществующим логином')
    def test_authorization_courier_non_existent_login(self):
        gen_data = generator()
        payload = {
            'login': gen_data.get('login'),
            'password': self.dict_registration.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Учетная запись не найдена"' in response.text and response.status_code == 404

    @allure.title('Отправляем POST запрос для авторизации ранее зарегистрированного курьера, с несуществующим паролем')
    def test_authorization_courier_non_existent_password(self):
        gen_data = generator()
        payload = {
            'login': self.dict_registration.get('login'),
            'password': gen_data.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Учетная запись не найдена"' in response.text and response.status_code == 404

    @allure.title('Отправляем POST запрос для авторизации курьера без логина')
    def test_authorization_courier_without_login(self):
        payload = {
            'login': '',
            'password': self.dict_registration.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Недостаточно данных для входа"' in response.text and response.status_code == 400

    @allure.title('Отправляем POST запрос для авторизации курьера без пароля')
    def test_authorization_courier_without_password(self):
        payload = {
            'login': self.dict_registration.get('login'),
            'password': ''
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Недостаточно данных для входа"' in response.text and response.status_code == 400

    @classmethod
    def teardown_class(cls):
        cls.payload = {
            'login': cls.dict_registration.get('login'),
            'password': cls.dict_registration.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=cls.payload)
        r = response.json()
        requests.delete(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}/{r.get('id')}')
