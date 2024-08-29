import allure
import requests
from utils.url import *
from utils.endpoint import *


class TestAuthorizationCourier:
    @allure.title('Отправляем POST запрос для авторизации ранее зарегистрированного курьера')
    def test_authorization_courier(self, default_user):

        payload = {
            'login': default_user.get('login'),
            'password': default_user.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert 'id' in response.text and response.status_code == 200

    @allure.title('Отправляем POST запрос для авторизации курьера с несуществующим логином')
    def test_authorization_courier_non_existent_login(self, generator, default_user):
        payload = {
                'login': generator.get('login'),
                'password': default_user.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Учетная запись не найдена"' in response.text and response.status_code == 404

    @allure.title('Отправляем POST запрос для авторизации ранее зарегистрированного курьера, с несуществующим паролем')
    def test_authorization_courier_non_existent_password(self, generator, default_user):
        payload = {
                'login': default_user.get('login'),
                'password': generator.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Учетная запись не найдена"' in response.text and response.status_code == 404

    @allure.title('Отправляем POST запрос для авторизации курьера без логина')
    def test_authorization_courier_without_login(self, default_user):
        payload = {
                'login': '',
                'password': default_user.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Недостаточно данных для входа"' in response.text and response.status_code == 400

    @allure.title('Отправляем POST запрос для авторизации курьера без пароля')
    def test_authorization_courier_without_login(self, default_user):
        payload = {
            'login': default_user.get('login'),
            'password': ''
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_COURIER}', data=payload)
        assert '"message":"Недостаточно данных для входа"' in response.text and response.status_code == 400
