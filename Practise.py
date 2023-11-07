import os
import datetime

class BankApplication:
    def __init__(self):
        self.data_file = "Bank Data.txt"
        self.transaction_directory = "Transaction Logs"
        self.current_transaction = None
        self.logged_in = False
        self.current_user = None

    def load_accounts(self):
        accounts = {}
        try:
            with open(self.data_file, "r") as file:
                for line in file:
                    full_name, pin, balance = line.strip().split(':')
                    accounts[full_name] = {"pin": pin, "balance": float(balance)}
        except FileNotFoundError:
            pass
        return accounts

    def save_accounts(self, accounts):
        with open(self.data_file, "w") as file:
            for full_name, account_info in accounts.items():
                file.write(f"{full_name}:{account_info['pin']}:{account_info['balance']}\n")

    def record_transaction(self, transaction_type, amount):
        if self.logged_in and self.current_user:
            user_transaction_file = f"{self.transaction_directory}/{self.current_user}_Transaction_Log.txt"
            formatted_amount = f"R{amount:.2f}"
            transaction_time = datetime.datetime.now()
            if transaction_type == "Deposit" or transaction_type == "Withdrawal":
                if amount <= 999:
                    transaction_fee = 1.50
                else:
                    transaction_fee = 5.50
            else:
                transaction_fee = 0.0
            with open(user_transaction_file, "a") as file:
                file.write(f"{transaction_time} - {transaction_type}: {formatted_amount} with :R{transaction_fee} \n")

    def display_balance(self):
        if self.logged_in and self.current_user:
            print(f"Current Balance for {self.current_user}: R{self.accounts[self.current_user]['balance']:.2f}")

    def print_statement(self):
        if self.logged_in and self.current_user:
            user_transaction_file = f"{self.transaction_directory}/{self.current_user}_Transaction_Log.txt"
            try:
                with open(user_transaction_file, "r") as file:
                    print(f"\n\nTransaction History for {self.current_user}:\n\n")
                    transactions = file.read().strip().split('\n')
                    for transaction in transactions:
                        print(transaction)
            except FileNotFoundError:
                print(f"No transaction history available for {self.current_user}.")
        else:
            print("No user is logged in.")

    def create_account(self):
        while True:
            full_name = input("Enter your username: ")
            if len(full_name) >= 4 and len(full_name) <= 10 and full_name.isalnum():
                break
            else:
                print("Invalid input. Please enter a username with letters and numbers only, 4-10 characters.")
        
        while True:
            pin_str = input("Enter your PIN (4 digits only): ")
            if pin_str.isdigit() and len(pin_str) == 4:
                pin = int(pin_str)
                break
            else:
                print("Invalid input. Please enter a PIN consisting of 4 only numeric digits.")


        if full_name in self.accounts:
            print("Account already exists.")
            return

        self.accounts[full_name] = {"pin": pin, "balance": 0.0}
        self.save_accounts(self.accounts)

        user_transaction_file = f"{self.transaction_directory}/{full_name}_Transaction_Log.txt"
        with open(user_transaction_file, "w") as file:
            pass

        print("Account created successfully.")

    def login(self):
        while True:
            full_name = input("Enter your username: ")
            if len(full_name) >= 4 and len(full_name) <= 10 and full_name.isalnum():
                break
            else:
                print("Invalid input. Please enter a username with letters and numbers only, 4-10 characters.")
        
        while True:
            pin_str = input("Enter your PIN (4 digits only): ")
            if pin_str.isdigit() and len(pin_str) == 4:
                pin = int(pin_str)
                break
            else:
                print("Invalid input. Please enter a PIN consisting of 4 only numeric digits.")




        if full_name in self.accounts and self.accounts[full_name]["pin"] == pin:
            print("Login successful.")
            self.logged_in = True
            self.current_user = full_name
        else:
            print("Login failed.\n Please check your Username and PIN.")

    def start(self):
        self.accounts = self.load_accounts()
        if not os.path.exists(self.transaction_directory):
            os.makedirs(self.transaction_directory)

        print("Welcome to the C bank")
        while True:
            try:
                if not self.logged_in:
                    action = input("What would you like to do?\n\n\n1. Account\n2. Login\n3. Exit\n\nEnter 1, or 2, or 3 : ")
                    if action == "1":
                        self.create_account()
                    elif action == "2":
                        self.login()
                    elif action == "3":
                        break
                    else:
                        print("Invalid input. Please enter '1', or '2', or '3'.")
                else:
                    transaction = input("Would you like to make a transaction? (Y/N): ").upper()
                    if transaction == "Y":
                        action = input("Which transaction would you like to make?\n\n\n1.Deposit\n2.Withdraw\n3.Statement\n\nEnter 1, or 2, or 3 : ")
                        if action not in ["1", "2", "3"]:
                            print("Invalid action. Please enter '1',or '2', or '3'.")
                            continue

                        if action == "1":
                            amount = float(input("How much would you like to deposit? R"))
                            if amount <= 0:
                                print("Invalid deposit amount. Please enter a positive amount.")
                                continue

                            if amount <= 999:
                                transaction_fee = 1.50
                            else:
                                transaction_fee = 5.50

                            total_amount = amount - transaction_fee

                            self.accounts[self.current_user]["balance"] += total_amount
                            self.save_accounts(self.accounts)
                            self.record_transaction("Deposit", total_amount)
                            print(f"Deposit of R{amount:.2f} was successful. Transaction Fee: R{transaction_fee:.2f}.\n")

                        elif action == "2":
                            amount = float(input("How much would you like to withdraw? R"))
                            if amount <= 0:
                                print("Invalid withdrawal amount. Please enter a positive amount.")
                                continue

                            if amount <= 999:
                                transaction_fee = 1.50
                            else:
                                transaction_fee = 5.50

                            if amount + transaction_fee > self.accounts[self.current_user]["balance"]:
                                print("Insufficient balance. ")
                                continue

                            total_amount = amount + transaction_fee

                            self.accounts[self.current_user]["balance"] -= total_amount
                            self.save_accounts(self.accounts)
                            self.record_transaction("Withdrawal", total_amount)
                            print(f"Withdrawal of R{amount:.2f} was successful. Transaction Fee: R{transaction_fee:.2f}. Current balance: R{self.accounts[self.current_user]['balance']:.2f}")

                        elif action == "3":
                            self.print_statement()

                        self.display_balance()

                    elif transaction == "N":
                        self.logged_in = False
                        self.current_user = None
                    else:
                        print("Invalid input. Please enter 'Y' or 'N'.")

            except ValueError:
                print("You provided an invalid input.")

        print("Thank you for using the Bank Application. Goodbye!")

if __name__ == "__main__":
    bank_app = BankApplication()
    bank_app.start()
