import allure
import requests
from utils.url import *
from utils.endpoint import *


class TestCreateCourier:
    @allure.title('Отправляем POST запрос на создание курьера с неиспользованными ранее данными')
    def test_create_courier(self, generator):
        payload = {
            'login': generator.get('login'),
            'password': generator.get('password'),
            'first_name': generator.get('first_name')
        }
        correct_response_body = '{"ok":true}'
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert response.text == correct_response_body and response.status_code == 201

    @allure.title('Отправляем POST запрос на создание курьера с данными, которые уже есть в системе')
    def test_create_identical_courier(self, default_user):

        payload = {
            'login': default_user.get('login'),
            'password': default_user.get('password'),
            'first_name': default_user.get('first_name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert 'Этот логин уже используется' in response.text and response.status_code == 409

    @allure.title('Отправляем POST запрос на создание курьера без логина')
    def test_create_courier_without_login(self, generator):

        payload = {
            'login': '',
            'password': generator.get('password'),
            'first_name': generator.get('first_name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert 'Недостаточно данных для создания учетной записи' in response.text and response.status_code == 400

    @allure.title('Отправляем POST запрос на создание курьера без пароля')
    def test_create_courier_without_password(self, generator):

        payload = {
            'login': generator.get('login'),
            'password': '',
            'first_name': generator.get('first_name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_COURIER}', data=payload)
        assert 'Недостаточно данных для создания учетной записи' in response.text and response.status_code == 400
