import mysql.connector
import uuid 

class DatabaseManager:
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


