#
from services.currency_service import CurrencyAPIProxy
from services.token_service import TokenService

from singleton import ConfigManager, DatabaseManager, SessionManager
from facade import PortfolioFacade
from utils.db_helpers import DBHelpersFactory
from login_register import login_or_register, logout

config_manager = ConfigManager()
helper_factory = DBHelpersFactory()
session_manager = SessionManager()
portfolio_facade = PortfolioFacade()

db = DatabaseManager()
conn = db.connect()

print("\n")
print("Token-Tracker")
print("********************")
print("\n")

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
    # portfolio_facade.main_menu()

    currency_proxy = CurrencyAPIProxy()
    # print(currency_proxy.get_exchange_rate('EUR,CAD,USD,CNY,GBP,AUD,JPY'))
    token_service = TokenService()
    token_service.view_top_tokens()

    
    # view portfolio
        # view token details
            # add token to portfolio
            # remove token from portfolio
        # Sort by metric

    # Observe tokens prices
    # observer()

    # Total porfolio value

    # Change fiat currency

    # View top tokens

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
print("\n")
print('Goodbye')