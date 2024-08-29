import json
import allure
import pytest
import requests
from utils.url import *
from utils.endpoint import *


class TestCreateOrder:
    @allure.title('Отправляем POST запрос для создания заказа с использованием параметризации')
    @pytest.mark.parametrize('color', [[None], ['GREY'], ['BLACK'], ['BLACK', 'GREY']])
    def test_create_order(self, color, generator_order):
        order = generator_order
        order['color'] = color
        payload = json.dumps(order)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}', data=payload, headers=headers)
        assert '"track":' in response.text and response.status_code == 201
