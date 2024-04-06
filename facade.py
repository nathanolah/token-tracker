################################################################################
# Facade Design Pattern
#
# Purpose: The facade pattern is used to provide an interface for various
# services such as the token and currency service. Combining their 
# functionality into once unified interface for users to interact and
# execute application operations.
# 
# Student Name: Nathan Olah
# Student ID: 400493296
# https://github.com/nathanolah/token-tracker
#
################################################################################

class PortfolioFacade:
    def __init__(self, session_manager, token_service, currency_service, user_observer):
        self.session_manager = session_manager
        self.token_service = token_service
        self.currency_service = currency_service
        self.user_observer = user_observer
        
    def main_menu(self):
        session = self.session_manager.get_current_session()
        username = session[1] # Get username from current session

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
                self.user_observer.observer()
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
            print("4. Go Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.token_service.view_tokens(username, "view") # View tokens option
            elif choice == "2":
                self.token_service.add_token_to_portfolio(username)
            elif choice == "3":
                self.token_service.view_tokens(username, "remove") # Remove token option
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
