from singleton import SessionManager
from utils.db_helpers import DBHelpersFactory
import getpass
import bcrypt

session_manager = SessionManager()
helper_factory = DBHelpersFactory()
user_helper = helper_factory.create_helper('user')

def login_or_register():
    while True:
        choice = input("Login or Register? (login/register): ").lower()
        if choice == "login":
            username = login()
            if username:
                return username
        elif choice == "register":
            register()
        else:
            print("Invalid choice. Please enter 'login' or 'register'.")

# Find if username exists
def check_username(username):
    return user_helper.select_user(username) is not None

def register():
    while True:
        username = input('Enter username: ')
        if check_username(username):
            print('Username already exists. Please choose another one.')
        else:
            break

    password = getpass.getpass('Enter password: ')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_helper.insert(username, hashed_password)
    print('Registration was successful!')

def login():
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    result = user_helper.select_hashed_password(username)

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