#
################################################################################
from observer import observer
# from singleton import SessionManager
# from services.currency_service import CurrencyAPIProxy
# from services.token_service import TokenService

class PortfolioFacade:
    def __init__(self, session_manager, token_service, currency_service):
        self.session_manager = session_manager
        self.token_service = token_service
        self.currency_service = currency_service
        # self.session_manager = SessionManager()
        # self.token_service = TokenService()
        # self.currency_service = CurrencyAPIProxy()
        
    def main_menu(self):
        session = self.session_manager.get_current_session()
        username = session[1]

        while True:
            print("Main Menu:")
            print("1. View Portfolio")
            print("2. View Top Ethereum Tokens")
            print("3. Observe Tokens Prices")
            print("4. Calculate Total Portfolio")
            print("5. Change Fiat Currency") 
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_portfolio_menu(username)
            elif choice == "2":
                self.token_service.view_top_tokens(username)
            elif choice == "3":
                observer()
            elif choice == "4":
                self.token_service.calculate_portfolio(username)
            elif choice == "5":
                self.currency_service.change_currency()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")


    def view_portfolio_menu(self, username):
        while True:
            print("Portfolio Menu:")
            print("1. View Tokens in Portfolio")
            print("2. Add Token to Portfolio")
            print("3. Remove Token from Portfolio")
            print("4. Sort by Metric")
            print("5. Go Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.token_service.view_tokens(username, "view")
            elif choice == "2":
                self.token_service.add_token_to_portfolio(username)
            elif choice == "3":
                self.token_service.view_tokens(username, "remove")
            elif choice == "4":
                print('sort by metric')
                # self.sort_by_metric()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
