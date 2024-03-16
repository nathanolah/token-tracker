#
################################################################################
from services.currency_service import CurrencyAPIProxy
from services.token_service import TokenService
from singleton import ConfigManager, CurrencyManager, DatabaseManager, SessionManager
from facade import PortfolioFacade
from utils.db_helpers import DBHelpersFactory
from utils.login_register import login_or_register, logout

# Setup
config_manager = ConfigManager()
currency_manager = CurrencyManager()
helper_factory = DBHelpersFactory()
session_manager = SessionManager()
token_service = TokenService()
currency_service = CurrencyAPIProxy()
portfolio_facade = PortfolioFacade(session_manager, token_service, currency_service)

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