################################################################################
# Observer Design Pattern
#
# Purpose: The observer tracks real-time price data for each token in the 
# user's portfolio by fetching price updates and notifying the user when
# a price change occurs.
# 
# Student Name: Nathan Olah
# Student ID: 400493296
# https://github.com/nathanolah/token-tracker
#
################################################################################
from abc import ABC, abstractmethod
import requests
import threading
from services.currency_service import CurrencyAPIProxy
from singleton import CurrencyManager, SessionManager, ConfigManager
from utils.db_helpers import DBHelpersFactory

config_manager = ConfigManager()
session_manager = SessionManager()
currency_manager = CurrencyManager()
moralis_api_key = config_manager.get_moralis_api_key()

class Subject(ABC):
    @abstractmethod
    def register_observer(self, observer):
        pass
    
    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass

class Observer(ABC):
    @abstractmethod
    def update(self, token):
        pass

# Concrete Subject
class Token(Subject):
    def __init__(self, name, price, address):
        self._name = name
        self._price = price
        self._address = address
        self.observers = []

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def address(self):
        return self._address

    # Checks for a change in price, sets new price and notifies observer
    def set_price(self, price):
        if self._price != price:
            self._price = price
            self.notify_observers()

    # Register an observer for the token
    def register_observer(self, observer):
        self.observers.append(observer)

    # Remove an observer for the token
    def remove_observer(self, observer):
        self.observers.remove(observer)

    # Notify observers
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

class TokenObserver:
    def __init__(self, user, moralis_api_key):
        self.user = user
        self.moralis_api_key = moralis_api_key
        self.event = threading.Event()
        self.currency_service = CurrencyAPIProxy()
    
    def fetch_token_data(self, address):
        headers = { 
                    "accept": "application/json",
                    "X-API-Key": self.moralis_api_key
                }
        res = requests.get(f"https://deep-index.moralis.io/api/v2.2/erc20/{address}/price", headers=headers)
        token_data = res.json()
        return token_data

    def observe_tokens(self):
        while not self.event.is_set():
            for token in self.user.tokens:
                try:
                    data = self.fetch_token_data(token.address)
                    converted_price = self.currency_service.convert_value(data['usdPriceFormatted'])
                    token.set_price(converted_price)
                    # print(f"Fetching: {token.address} | Token: {token.name} | Price: {token.price}")
                except requests.RequestException as e:
                    print(f"Error fetching token info for {token.address}: {e}")
                except KeyError as e:
                    print(f"Error parsing token info for {token.address}: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
            
            self.event.wait(timeout=25)

    def stop_observing(self):
        # Stop thread 
        self.event.set()

# Concrete Observer
class User(Observer):
    def __init__(self, name):
        self.name = name
        self.tokens = []
        self.currency_service = CurrencyAPIProxy()
    
    def fetch_token_data(self, address):
        headers = { 
                    "accept": "application/json",
                    "X-API-Key": moralis_api_key
                }
        res = requests.get(f"https://deep-index.moralis.io/api/v2.2/erc20/{address}/price", headers=headers)
        token_data = res.json()
        return token_data

    def update(self, token):
        # Log token changes to the user
        print(f"Hello {self.name}, {token.name} price changed to {token.price} {currency_manager.get_currency()}.")

    def add_token(self, token):
        self.tokens.append(token)
        token.register_observer(self)

    def observe_tokens(self):
        # Spawn a new thread for observing. the main thread is waiting for the user to stop.
        observer = TokenObserver(self, moralis_api_key)
        thread = threading.Thread(target=observer.observe_tokens)
        thread.start()

        input("Press Enter to stop observing tokens...\n")

        observer.stop_observing()
        thread.join()

    def observer(self):
        # Get username from current session and retrive user's portfolio tokens
        username = session_manager.get_username(session_manager.get_current_session()[0])
        user_helper = DBHelpersFactory().create_helper('user')
        tokenData = user_helper.retrive_tokens(username)

        # Gather the list of token addresses
        tokenList = [token[0] for token in tokenData]

        if not tokenList:
            print(f'{username} has no tokens in their portfolio')
        else:
            # Fetch token data for each token and add to current user for observer
            currentUser = User(username)
            for token in tokenList:
                data = self.fetch_token_data(token)
                
                # Covert price to set currency
                converted_price = self.currency_service.convert_value(data['usdPriceFormatted'])
                
                newToken = Token(data['tokenName'], converted_price, data['tokenAddress'])
                currentUser.add_token(newToken)
            
            # Begin observing tokens
            currentUser.observe_tokens()
