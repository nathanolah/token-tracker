################################################################################
import mysql.connector
from mysql.connector import errorcode
from singleton import DatabaseManager

db = DatabaseManager()
conn = db.connect()
cursor = conn.cursor()

class DBHelpersFactory:
    @staticmethod
    def create_helper(helper_type):
        if helper_type == 'user':
            return UserDBHelper()
        elif helper_type == 'token':
            return TokenDBHelper()
        else:
            raise ValueError('Invalid helper type')
        
class DBHelpers:
    def insert(self):
        raise NotImplementedError('SQL operation must be implemented in subsclasses')
    
class UserDBHelper(DBHelpers):
    # Insert new user into db
    def insert(self, username, password):
        sql = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        val = (username, password)
        try:
            cursor.execute(sql, val)
            conn.commit()
            print('User inserted successfully.')
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print(f"Error: User '{username}' already exists.")
            else:
                print(f'Error: {err}')
    
    # Select user id
    def get_user_id(self, username):
        sql = 'SELECT user_id FROM users WHERE username = %s'
        try:
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the user ID
            else:
                print(f"User '{username}' not found.")
                return None
                
        except mysql.connector.Error as err:
            print(f'Error retrieving user ID: {err}')
            return None
    
    # Select token id
    def get_token_id(self, token_address):
        sql = 'SELECT token_id FROM tokens WHERE token_address = %s'
        try:
            cursor.execute(sql, (token_address,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the token ID
            else:
                print(f"Token with address '{token_address}' not found.")
                return None
            
        except mysql.connector.Error as err:
            print(f'Error retrieving token ID: {err}')
            return None

    # Remove token for user
    def remove_token_for_user(self, username, token_address):
        user_id = self.get_user_id(username)
        token_id = self.get_token_id(token_address)

        if user_id is None or token_id is None:
            return  # Exit if either user or token is not found

        sql = 'DELETE FROM user_tokens WHERE user_id = %s AND token_id = %s'
        try:
            cursor.execute(sql, (user_id, token_id))
            conn.commit()
            print('Token removed from user successfully.')
        except mysql.connector.Error as err:
            print(f'Error removing token from user: {err}')

    # Select user
    def select_user(self, username):
        sql = 'SELECT username from users WHERE username = %s'
        cursor.execute(sql, (username,))
        return cursor.fetchone()
    
    # Select users hashed password
    def select_hashed_password(self, username):
        sql = 'SELECT password FROM users WHERE username = %s'
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        return result

    # Retrive users tokens in portfolio
    def retrive_tokens(self, username):
        sql = '''
                SELECT tokens.token_address 
                FROM users
                JOIN user_tokens ON users.user_id = user_tokens.user_id
                JOIN tokens ON user_tokens.token_id = tokens.token_id
                WHERE users.username = %s
            '''
        try:
            cursor.execute(sql, (username,))
            tokens = cursor.fetchall()
            if not tokens:
                print(f"User: '{username}' no tokens found")

            return tokens
        except mysql.connector.Error as err:
            print(f'Error: {err}')

    # Associate a user with a token (add to user's portfolio)
    def insert_token_for_user(self, user_id, token_id):
        sql = 'INSERT INTO user_tokens (user_id, token_id) VALUES (%s, %s)'
        try:
            cursor.execute(sql, (user_id, token_id))
            conn.commit()
            # print('Token associated with user successfully.')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print("This token is already in your portfolio")
                # print(f"Error: user id: {user_id} is already associated with token id: {token_id}")
            else:
                print(f'Error: {err}') 
   
    # Add token to user's portfolio
    def add_token_to_portfolio(self, username, token_address):
        try:
            token_id = None
            sql = 'SELECT token_id FROM tokens WHERE token_address = %s'
            cursor.execute(sql, (token_address,))
            result = cursor.fetchone()

            if result:
                token_id = result[0]
                # print("Token already exists. Token ID:", token_id)
            else:
                # Token not found, insert token
                sql = 'INSERT INTO tokens (token_address) VALUES (%s)'
                cursor.execute(sql, (token_address,))
                conn.commit()
                token_id = cursor.lastrowid
                # print("Token inserted. Token ID:", token_id)

            sql = 'SELECT user_id FROM users WHERE username = %s'
            cursor.execute(sql, (username,))
            user_id = cursor.fetchone()[0]

            self.insert_token_for_user(user_id, token_id)
        
        except mysql.connector.Error as err:
            print(f'Error: {err}')

class TokenDBHelper(DBHelpers):
    # Insert new token by token address into db
    def insert(self, token_address):
        sql = 'INSERT INTO tokens (token_address) VALUES (%s)'
        try:
            cursor.execute(sql, (token_address,))
            conn.commit()
            print('Token inserted successfully.')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print(f"Error: Token '{token_address}' already exists")
            else:
                print(f'Error: {err}')

# 
# Database Setup/Reset
#
def reset_database():
    cmd = input('Are you sure you want to reset the database y/n?')
    if (cmd == 'y'):
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('DROP TABLE IF EXISTS tokens')
        cursor.execute('DROP TABLE IF EXISTS user_tokens')

        sql = '''CREATE TABLE users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY, 
                    username VARCHAR(255) UNIQUE, 
                    password VARCHAR(255)
                )'''
        cursor.execute(sql)

        sql = '''CREATE TABLE tokens (
                    token_id INT AUTO_INCREMENT PRIMARY KEY, 
                    token_address VARCHAR(255) UNIQUE
                )'''
        cursor.execute(sql)

        sql = '''CREATE TABLE user_tokens (
                    user_id INT,
                    token_id INT, 
                    FOREIGN KEY (user_id) REFERENCES users(user_id), 
                    FOREIGN KEY (token_id) REFERENCES tokens(token_id),
                    PRIMARY KEY (user_id, token_id)     
                )'''
        cursor.execute(sql)