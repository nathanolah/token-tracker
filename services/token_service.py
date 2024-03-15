#
################################################################################
import requests
from singleton import SessionManager, ConfigManager, CurrencyManager
from utils.db_helpers import DBHelpersFactory
from services.currency_service import CurrencyAPIProxy

config_manager = ConfigManager()
currency_manager = CurrencyManager()
session_manager = SessionManager()
helper_factory = DBHelpersFactory()
currency_service = CurrencyAPIProxy()

user_helper = helper_factory.create_helper('user')
ethplorer_api_key = config_manager.get_ethplorer_api_key()

class TokenService():
    # View top Ethereum tokens
    def view_top_tokens(self, username):
        res = requests.get(f"https://api.ethplorer.io/getTopTokens?apiKey={ethplorer_api_key}")
        data = res.json()

        if 'tokens' in data:
            for i, token in enumerate(data['tokens'], 1):
                # Check if 'name' key exists in the token
                name = token.get('name', "N/A")

                # Check if 'symbol' key exists in the token
                symbol = token.get('symbol', "N/A")

                # Check if 'address' key exists in the token
                address = token.get('address', "N/A")

                # Check if 'price' key exists in the token and if it's a dictionary
                price = token['price'].get('bid', "N/A") if isinstance(token.get('price'), dict) else "N/A"

                # Check if 'marketCapUsd' key exists in the 'price' dictionary
                market_cap_usd = token['price'].get('marketCapUsd', "N/A") if isinstance(token.get('price'), dict) else "N/A"

                converted_price = currency_service.convert_value(price)
                converted_mc = currency_service.convert_value(market_cap_usd)
                currency_type = currency_manager.get_currency()

                if converted_price:
                    formatted_price = "{:.8f}".format(converted_price)

                # Print token information
                print(f"{i}. Token: {name} ({symbol}) | Price: ${formatted_price} {currency_type} | Market Cap: ${converted_mc} {currency_type} | Address: {address}")

        while True:
            # Get user input for token selection
            choice = input("Select a token number to add to your portfolio (or 'q' to go back): ")

            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(data['tokens']):
                    token_address = data['tokens'][choice - 1].get('address')
                    user_helper.add_token_to_portfolio(username, token_address)
                    print("Token added to portfolio successfully.")
                    break
                else:
                    print("Invalid token number.")
            elif choice.lower() == 'q':
                break
            else:
                print("Invalid input. Please enter a valid token number or 'q' to go back.")
 
    # Calculate total portfolio value, based on given token amounts
    def calculate_portfolio(self, username):
        total_balance = 0
        tokenData = user_helper.retrive_tokens(username)
        tokenList = [token[0] for token in tokenData]

        if not tokenList:
            print(f"{username} has no tokens in their portfolio")
        else:
            print(f"{username}'s Portfolio")
            for i, token in enumerate(tokenList, 1):
                res = requests.get(f"https://api.ethplorer.io/getTokenInfo/{token}?apiKey={ethplorer_api_key}")
                data = res.json()

                price = float(data['price']['bid'])
                formatted_price = "{:.8f}".format(price)
                name = data['name']
                address = data['address']
                print(f"{i}. Token name: {name} | Price: {formatted_price} | Address: {address}")
                
                while True:
                    try:
                        tokenQuantity = float(input(f"Please enter token amount for {name}: "))
                        break
                    except ValueError:
                        print("Please enter a valid number.")

                # Calculate total balance for this token
                total_balance += price * tokenQuantity

            print(f'Total Portfolio Balance: {total_balance}')

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

    # Remove token from user's portfolio
    def remove_token_from_portfolio(self, username, selected_token):
        user_helper.remove_token_for_user(username, selected_token)

    # View detailed token information and market data
    def view_token_details(self, token):
        # Request token details
        res = requests.get(f"https://api.ethplorer.io/getTokenInfo/{token}?apiKey={ethplorer_api_key}")
        data = res.json()

        # Extract token details
        print(data)
        input("Press Enter to continue...")

    # List user's portfolio tokens
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