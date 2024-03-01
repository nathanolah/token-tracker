##
#
from observer import observer
from singleton import DatabaseManager, SessionManager
from utils.db_helpers import DBHelpers
from login_register import register, login, logout

print("\n")
print("Token-Tracker")
print("********************")

db = DatabaseManager()
conn = db.connect()
mycursor = conn.cursor()

db_helpers = DBHelpers()
session_manager = SessionManager()

# Login/Sign-up

# register()

notDone = True
while notDone:
    username = login()
    if username is None:
        cmd = input("Try again? y/n: ")
        if cmd != 'y':
            notDone = False
    else:
        notDone = False

# create session passing in the username, so we have a globally accessible session id
if username:
    session_id = session_manager.create_session(username)

    # print(session_id)
    # print(session_manager.get_username(session_id))

    # print(session_manager.get_current_session())

    logout()


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

