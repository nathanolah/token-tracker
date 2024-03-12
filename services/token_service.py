import requests
from singleton import SessionManager, ConfigManager
from utils.db_helpers import DBHelpersFactory

config_manager = ConfigManager()
session_manager = SessionManager()
helper_factory = DBHelpersFactory()

user_helper = helper_factory.create_helper('user')
ethplorer_api_key = config_manager.get_ethplorer_api_key()

class TokenService():
    # Perform validation checks on the token address
    def validate_token_address(self, token_address):
        return len(token_address) == 42 and token_address.startswith("0x")

    #
    def add_token_to_portfolio(self, username):
        # Get the token address from the user
        token_address = input("Enter the token's contract address: ")

        if not self.validate_token_address(token_address):
            print("Invalid token address. Please enter a valid Ethereum token contract address.")
            return

        # Attempt to add the token to the user's portfolio
        try:
            user_helper.add_token_to_portfolio(username, token_address)
            print("Token added to portfolio successfully.")
        except Exception as e:
            print(f"Error adding token to portfolio: {e}")

    #
    def remove_token_from_portfolio(self, username, selected_token):
        user_helper.remove_token_for_user(username, selected_token)

    #
    def view_token_details(self, token):
        # Request token details
        res = requests.get(f"https://api.ethplorer.io/getTokenInfo/{token}?apiKey={ethplorer_api_key}")
        data = res.json()

        # Extract token details
        print(data)
        input("Press Enter to continue...")

    #
    def view_tokens(self, username, option):
        # Get all the user's tokens from the db
        tokenData = user_helper.retrive_tokens(username)
        tokenList = [token[0] for token in tokenData]

        if not tokenList:
            print(f'{username} has no tokens in their portfolio')
        else:
            while True:
                print("Tokens in portfolio")
                for i, token in enumerate(tokenList, 1):
                    res = requests.get(f"https://api.ethplorer.io/getTokenInfo/{token}?apiKey={ethplorer_api_key}")
                    data = res.json()

                    price = float(data['price']['bid'])
                    formatted_price = "{:.8f}".format(price)
                    name = data['name']
                    address = data['address']
                    print(f'{i}. Token name: {name} | Price: {formatted_price} | Address: {address}')

                if option == "view":
                    choice = input("Enter the number of the token to view details (or 'q' to quit): ")
                elif option == "remove":
                    choice = input("Enter the number of the token to remove (or 'q' to quit): ")

                if choice.lower() == 'q':
                    break

                try:
                    index = int(choice) - 1
                    selected_token = tokenList[index]
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid number.")
                    continue

                if option == "view":
                    self.view_token_details(selected_token)
                elif option == "remove":
                    # Remove the token from the user's portfolio
                    self.remove_token_from_portfolio(username, selected_token)
                    # Update the token list after removal
                    tokenList.remove(selected_token)