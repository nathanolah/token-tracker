#
################################################################################
from singleton import ConfigManager, CurrencyManager, DatabaseManager, SessionManager
from facade import PortfolioFacade
from utils.db_helpers import DBHelpersFactory
from login_register import login_or_register, logout

config_manager = ConfigManager()
helper_factory = DBHelpersFactory()
session_manager = SessionManager()
currency_manager = CurrencyManager()
portfolio_facade = PortfolioFacade()

db = DatabaseManager()
conn = db.connect()

print("\n")
print("Token-Tracker")
print("********************")

not_done = True
while not_done:
    username = login_or_register()
    if username is None:
        cmd = input("Try again? (y/n): ").lower()
        if cmd != 'y':
            not_done = False
    else:
        not_done = False

if username:
    # create session passing in the username, so we have a globally accessible session id
    session_id = session_manager.create_session(username)
    portfolio_facade.main_menu()
    # view portfolio
        # view token details
            # add token to portfolio
            # remove token from portfolio
        # Sort by metric

    # Observe tokens prices
    # observer()

    logout()

db.close()
print('Goodbye.')