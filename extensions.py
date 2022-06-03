import requests
import json
from database import keys

class APIException(Exception):
    pass

#Обработка ошибок ввода пользователя
class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Ошибка в названии валюты {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Ошибка в названии валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверно указано количество {amount}')

        #запрос с сервиса cryptocompare
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        #считывание базы данных доступных валют
        total_base = json.loads(r.content)[keys[base]]

        return total_base