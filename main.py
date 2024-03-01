##
#
import requests

from observer import observer
from singleton import DatabaseConnection
from utils.db_helpers import DBHelpers

print("\n")
print("Token-Tracker")
print("********************")

db = DatabaseConnection()
conn = db.connect()
mycursor = conn.cursor()

db_helpers = DBHelpers()

# Login/Sign-up




# Insert User
# db_helpers.insert_user("john123", "doe123")

# Insert Token
# db_helpers.insert_token("0x6982508145454Ce325dDbE47a25d4ec3d2311933")

# Insert token for a user
# db_helpers.insert_token_for_user(7,1)

# Retrive tokens for a user by username
# tokens = db_helpers.retrive_tokens_for_user('user123')
# print('Tokens for user:')
# for token in tokens:
#     print(token[0])

# Remove token for a user
# db_helpers.add_token_for_user('user123', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')


db.close()


# cmd = input("Would you like to observe list of tokens y/n: ")
# if (cmd == 'y'):
#     observer()

print('goodbye')

