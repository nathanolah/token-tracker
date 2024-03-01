from singleton import DatabaseManager, SessionManager
from utils.db_helpers import DBHelpers
import getpass
import bcrypt

db = DatabaseManager()
conn = db.connect()
cursor = conn.cursor()

db_helpers = DBHelpers()
session_manager = SessionManager()

# Find if username exists
def check_username(username):
    sql = 'SELECT username from users WHERE username = %s'
    cursor.execute(sql, (username,))
    return cursor.fetchone() is not None

def register():
    while True:
        username = input('Enter username: ')
        if check_username(username):
            print('Username already exists. Please choose another one.')
        else:
            break

    password = getpass.getpass('Enter password: ')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    db_helpers.insert_user(username, hashed_password)
    print('Registration was successful!')

def login():
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')

    sql = 'SELECT password FROM users WHERE username = %s'
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print('Login successful')
            return username
        else:
            print('Invalid username or password')
            return None
    else:
        print('Invalid username or password')
        return None
    
def logout():
    session_id = session_manager.get_current_session()
    session_manager.destroy_session(session_id)