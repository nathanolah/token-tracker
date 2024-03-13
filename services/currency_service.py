import requests
from abc import ABC, abstractmethod

# https://api.currencyapi.com/v3/latest?apikey=cur_live_iQpLlAOxaSwUNg7UFDuJZw2DBLDqP6ZSON19I45t&currencies=EUR%2CUSD%2CCAD

class CurrencyService(ABC):
    
    @abstractmethod
    def get_exchange_rate(self, base_currency, target_currency):
        pass

