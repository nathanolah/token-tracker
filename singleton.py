################################################################################
# Singleton Design Pattern
#
# Purpose: The singleton pattern manages aspects of the application such as,
# configuration, currency preferences, database connections, and user sessions.
# Each manager is separated by their use case to maintain simplicity. 
# 
# Student Name: Nathan Olah
# Student ID: 400493296
# https://github.com/nathanolah/token-tracker
#
################################################################################
import mysql.connector
import uuid 
import configparser

class ConfigManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.config = configparser.ConfigParser()
            cls._instance.config.read('config.server.cfg')
        return cls._instance
    
    def get_ethplorer_api_key(self):
        return self.config['API']['ethplorer_api_key']
    
    def get_moralis_api_key(self):
        return self.config['API']['moralis_api_key']
    
    def get_currency_api_key(self):
        return self.config['API']['currency_api_key']
    
class CurrencyManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.currency = "USD"
        return cls._instance

    def get_currency(self):
        return self.currency
    
    def set_currency(self, new_currency):
        self.currency = new_currency

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
            cls._instance.config = configparser.ConfigParser()
            cls._instance.config.read('config.server.cfg')

        return cls._instance
    
    def connect(self):
        if not self._connection:
            self._connection = mysql.connector.connect(
                host = self.config.get('Database', 'host'),
                user = self.config.get('Database', 'user'),
                passwd = self.config.get('Database', 'passwd'),
                database = self.config.get('Database', 'database')
            )
            # print("Connected to MySQL database")
        
        return self._connection
    
    def close(self):
        if self._connection:
            self._connection.close()
            # print("MySQL connection closed")
            self._connection = None

class SessionManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.sessions = {} # Dictionary to store session data

        return cls._instance
    
    def create_session(self, username):
        session_id = str(uuid.uuid4()) # generate session ID
        self.sessions[session_id] = username
        return session_id

    def destroy_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_username(self, session_id):
        return self.sessions[session_id]
    
    def get_current_session(self):
        for session_id, username in self.sessions.items():
            return session_id, username
        return None, None # No active session found


