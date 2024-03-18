# Observer Design Pattern
#
################################################################################
from abc import ABC, abstractmethod
import requests
import threading
from singleton import SessionManager, ConfigManager
from utils.db_helpers import DBHelpersFactory

config_manager = ConfigManager()
session_manager = SessionManager()
ethplorer_api_key = config_manager.get_ethplorer_api_key()

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

    def set_price(self, price):
        # print(f"checking set prices {self._price} and {price}")
        if self._price != price:
            self._price = price
            self.notify_observers()

    def register_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

class TokenObserver:
    def __init__(self, user, ethplorer_api_key):
        self.user = user
        self.ethplorer_api_key = ethplorer_api_key
        self.event = threading.Event()
    
    def observe_tokens(self):
        while not self.event.is_set():
            for token in self.user.tokens:
                try:
                    res = requests.get(f"https://api.ethplorer.io/getTokenInfo/{token.address}?apiKey={self.ethplorer_api_key}")
                    data = res.json()
                    price = float(data['price']['bid'])
                    formatted_price = "{:.8f}".format(price)
                    token.set_price(formatted_price)
                    # print(f"Fetching: {token.address} | Token: {token.name} | Price: {token.price}")
                except requests.RequestException as e:
                    print(f"Error fetching token info for {token.address}: {e}")
                except KeyError as e:
                    print(f"Error parsing token info for {token.address}: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
            
            self.event.wait(timeout=25)

    def stop_observing(self):
        self.event.set()

# Concrete Observer
class User(Observer):
    def __init__(self, name):
        self.name = name
        self.tokens = []

    def update(self, token):
        print(f"Price update log: Hello {self.name}, {token.name} price changed to {token.price}.")

    def add_token(self, token):
        self.tokens.append(token)
        token.register_observer(self)

    def observe_tokens(self):
        observer = TokenObserver(self, ethplorer_api_key)
        thread = threading.Thread(target=observer.observe_tokens)
        thread.start()

        input("Press Enter to stop observing tokens...\n")

        observer.stop_observing()
        thread.join()

    def observer(self):
        username = session_manager.get_username(session_manager.get_current_session()[0])
        user_helper = DBHelpersFactory().create_helper('user')
        tokenData = user_helper.retrive_tokens(username)

        tokenList = [token[0] for token in tokenData]

        if not tokenList:
            print(f'{username} has no tokens in their portfolio')
        else:
            currentUser = User(username)

            for token in tokenList:
                res = requests.get(f"https://api.ethplorer.io/getTokenInfo/{token}?apiKey={ethplorer_api_key}")
                data = res.json()
                price = float(data['price']['bid'])
                formatted_price = "{:.8f}".format(price)

                newToken = Token(data['name'], formatted_price, data['address'])
                currentUser.add_token(newToken)
            
            currentUser.observe_tokens()
