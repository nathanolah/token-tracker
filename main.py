#
################################################################################
from singleton import ConfigManager, CurrencyManager, DatabaseManager, SessionManager
from facade import PortfolioFacade
from utils.db_helpers import DBHelpersFactory
from login_register import login_or_register, logout

# Setup
config_manager = ConfigManager()
helper_factory = DBHelpersFactory()
session_manager = SessionManager()
currency_manager = CurrencyManager()
portfolio_facade = PortfolioFacade()

# Database Setup
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
    # Create session for user
    session_manager.create_session(username)
    portfolio_facade.main_menu()
    logout()

db.close()
print('Goodbye.')