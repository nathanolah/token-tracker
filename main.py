#
from observer import observer
from singleton import SessionManager
from utils.db_helpers import DBHelpersFactory
from login_register import register, login, logout

helper_factory = DBHelpersFactory()
session_manager = SessionManager()

print("\n")
print("Token-Tracker")
print("********************")

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

not_done = True
while not_done:
    username = login_or_register()
    if username is None:
        cmd = input("Try again? (y/n): ").lower()
        if cmd != 'y':
            not_done = False
    else:
        not_done = False

# create session passing in the username, so we have a globally accessible session id
if username:
    session_id = session_manager.create_session(username)

    # view portfolio
        # view token details
            # add token to portfolio
            # remove token from portfolio
        # Sort by metric

    # Observe tokens prices

    # Total porfolio value

    # Change fiat currency

    print(session_id)
    print(session_manager.get_username(session_id))
    print(session_manager.get_current_session())

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

# db.close()

# cmd = input("Would you like to observe list of tokens y/n: ")
# if (cmd == 'y'):
#     observer()

print('goodbye')

