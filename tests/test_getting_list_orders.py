import allure
import requests
from utils.url import *
from utils.endpoint import *


class TestGettingListOrders:
    @allure.title('Отправка GET запроса для получения списка заказов')
    def test_getting_list_orders(self):
        response = requests.get(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}')
        assert 'orders' in response.json() and response.status_code == 200