################################################################################
# Proxy Design Pattern
# 
# Purpose: The Proxy Design Pattern is utilized with the currency service class
# to manage exchange rate data. This pattern allows us to fetch exchange rates
# once and then use a proxy to access the cached data for subsequent requests.
# This design is useful since we have a limited number of requests available.
#
################################################################################
import requests
from abc import ABC, abstractmethod
from singleton import ConfigManager, CurrencyManager

config_manager = ConfigManager()
currency_manager = CurrencyManager()
currency_api_key = config_manager.get_currency_api_key()

# Default base currency is USD
class CurrencyService(ABC):
    @abstractmethod
    def get_exchange_rate(self, target_currency):
        pass

class CurrencyAPIService(CurrencyService):
    def get_exchange_rate(self, target_currency):
        res = requests.get(f"https://api.currencyapi.com/v3/latest?apikey={currency_api_key}&currencies={target_currency}")

        if res.status_code == 200:
            data = res.json()
            return data['data']
        else:
            print('Failed to fetch exchange rate')
            return None

class CurrencyAPIProxy(CurrencyService):
    def __init__(self):
        self._real_service = CurrencyAPIService()
        self._exchange_rates = {}

    def get_exchange_rate(self):
        target_currency = currency_manager.get_currency()

        # Check if target currency is already cached.
        if target_currency in self._exchange_rates:
            return self._exchange_rates[target_currency]
        
        exchange_rate_data = self._real_service.get_exchange_rate(target_currency)
        if exchange_rate_data is not None:
            for currency, info in exchange_rate_data.items():
                self._exchange_rates[currency] = info['value']
        
        return self._exchange_rates.get(target_currency)
    
    def change_currency(self):
        available_currencies = ['EUR', 'CAD', 'USD', 'CNY', 'GBP', 'AUD', 'JPY']
        new_currency = input("Enter the new currency (EUR, CAD, USD, CNY, GBP, AUD, JPY): ").upper()

        if new_currency in available_currencies:
            currency_manager.set_currency(new_currency)
            print(f"Currency changed to {new_currency}")
        else:
            print("Invalid currency. Please choose from the available options.")
        # print(f"{currency_manager.get_currency()}: ${self.get_exchange_rate()}")

    def convert_value(self, value):
        try:
            # rate = self.get_exchange_rate() ## using during prod, limited api requests avaliable
            rate = 1
            return float(value) * rate
        except:
            return None
