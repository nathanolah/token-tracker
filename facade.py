#
################################################################################
from singleton import SessionManager
from observer import observer
from services.token_service import TokenService

# add into facade constructor
session_manager = SessionManager()
token_service = TokenService()

class PortfolioFacade:
    # def __init__(self):

    # TODO : build out the functions/services "TokenManager", "PortfolioManger"
    # PortfolioManager can consist of function interacting with the DB
    # TokenManager will interact with APIs and DB
        
    def main_menu(self):
        session = session_manager.get_current_session()
        username = session[1]

        while True:
            print("Main Menu:")
            print("1. View Portfolio")
            print("View Top Ethereum Tokens")#####
            print("2. Observe Tokens Prices")
            print("3. Calculate Total Portfolio")
            print("4. Change Fiat Currency") 
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_portfolio_menu(username)
            elif choice == "2":
                observer()
            elif choice == "3":
                token_service.calculate_portfolio(username)
            elif choice == "4":
                print('change fiat currency')
                # self.change_fiat_currency()
            elif choice == "5":
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
                token_service.view_tokens(username, "view")
            elif choice == "2":
                token_service.add_token_to_portfolio(username)
            elif choice == "3":
                token_service.view_tokens(username, "remove")
            elif choice == "4":
                print('sort by metric')
                # self.sort_by_metric()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
