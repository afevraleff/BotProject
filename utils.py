import requests
import json
from extensions import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(qoute: str, base: str, amount: str):
        if qoute == base:
            raise APIException('Указаны одинаковые валюты')
        try:
            qoute_ticker = keys[qoute]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {qoute}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except KeyError:
            raise APIException(f'Не удалось обрабоать количество {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={qoute_ticker}&tsyms={base_ticker}')
        return round(json.loads(r.content)[keys[base]] * int(amount), 3)
