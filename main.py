#
################################################################################
from singleton import DatabaseManager, SessionManager
from services.currency_service import CurrencyAPIProxy
from services.token_service import TokenService
from utils.login_register import login_or_register, logout
from facade import PortfolioFacade
from observer import User

def main():
    # Setup
    session_manager = SessionManager()
    token_service = TokenService()
    currency_service = CurrencyAPIProxy()
    
    # Database Setup
    db = DatabaseManager()
    
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
        session_manager.create_session(username)
        user_instance = User(username)
        portfolio_facade = PortfolioFacade(session_manager, token_service, currency_service, user_instance)
        portfolio_facade.main_menu()
        logout()

    db.close()
    print('Goodbye.')

if __name__ == "__main__":
    main()