import mysql.connector

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None

        return cls._instance
    
    def connect(self):
        if not self._connection:
            self._connection = mysql.connector.connect(
                host="bwrtgbx7mfrlbr5trwgr-mysql.services.clever-cloud.com",
                user="u0zrufutr82wpicp",
                passwd="7HrKpbNeaajoJbIYeNxs",
                database="bwrtgbx7mfrlbr5trwgr"
            )
            print("Connected to MySQL database")
        
        return self._connection
    
    def close(self):
        if self._connection:
            self._connection.close()
            print("MySQL connection closed")
            self._connection = None

