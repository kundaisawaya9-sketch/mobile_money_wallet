
import json


class Wallet:
    def __init__(self, owner, pin, balance=0):
        self.owner = owner
        self.pin = pin
        self.balance = balance
        self.transactions = []
        self.wrong_pin_attempts = 0
        self.locked = False

    def display_wallet(self):
        print("\n----- WALLET DETAILS -----")
        print("Owner:", self.owner)
        print("Balance: $", self.balance)
        print("Wallet Locked:", self.locked)

    def verify_pin(self, entered_pin):
        if self.locked:
            print("Your wallet is locked.")
            return False

        if entered_pin == self.pin:
            self.wrong_pin_attempts = 0
            print("Login successful!")
            return True
        else:
            self.wrong_pin_attempts += 1
            print("Incorrect PIN!")

            if self.wrong_pin_attempts == 3:
                self.locked = True
                print("Your wallet has been locked!")
            else:
                print("Attempts remaining:", 3 - self.wrong_pin_attempts)

            return False

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self.balance = round(self.balance + amount, 2)

        transaction = {
            "type": "Deposit",
            "amount": amount
        }

        self.transactions.append(transaction)

        print("\nDeposit successful!")
        print("Amount deposited: $", amount)
        print("New balance: $", self.balance)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        transaction_fee = 0.50
        total_amount = round(amount + transaction_fee, 2)

        if total_amount > self.balance:
            print("Insufficient balance!")
            print("You need: $", total_amount)
            return

        self.balance = round(self.balance - total_amount, 2)

        transaction = {
            "type": "Withdrawal",
            "amount": amount,
            "fee": transaction_fee
        }

        self.transactions.append(transaction)

        print("\nWithdrawal successful!")
        print("Amount withdrawn: $", amount)
        print("Transaction fee: $", transaction_fee)
        print("Total deducted: $", total_amount)
        print("Remaining balance: $", self.balance)

    def transfer(self, recipient_wallet, amount):
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")

        transaction_fee = 0.50
        total_amount = round(amount + transaction_fee, 2)

        if self == recipient_wallet:
            print("You cannot transfer money to your own wallet.")
            return

        if recipient_wallet.locked:
            print("The receiving wallet is locked.")
            return

        if total_amount > self.balance:
            print("Insufficient balance!")
            print("You need: $", total_amount)
            return

        self.balance = round(self.balance - total_amount, 2)

        recipient_wallet.balance = round(
            recipient_wallet.balance + amount, 2
        )

        sender_transaction = {
            "type": "Transfer sent",
            "amount": amount,
            "fee": transaction_fee,
            "recipient": recipient_wallet.owner
        }

        self.transactions.append(sender_transaction)

        receiver_transaction = {
            "type": "Transfer received",
            "amount": amount,
            "sender": self.owner
        }

        recipient_wallet.transactions.append(receiver_transaction)

        print("\nTransfer successful!")
        print("You sent: $", amount)
        print("Transaction fee: $", transaction_fee)
        print("Total deducted: $", total_amount)
        print("Your new balance: $", self.balance)
        print(recipient_wallet.owner, "received $", amount)

    def display_history(self):
        print("\n===== TRANSACTION HISTORY =====")
        print("Customer:", self.owner)

        if len(self.transactions) == 0:
            print("No transactions found.")
            return

        for number, transaction in enumerate(self.transactions, start=1):
            print("\nTransaction", number)
            print("Type:", transaction["type"])
            print("Amount: $", transaction["amount"])

            if "fee" in transaction:
                print("Fee: $", transaction["fee"])

            if "recipient" in transaction:
                print("Sent to:", transaction["recipient"])

            if "sender" in transaction:
                print("Received from:", transaction["sender"])

        print("\nCurrent balance: $", self.balance)


wallets = []


def save_wallets():
    wallet_data = []

    for wallet in wallets:
        wallet_details = {
            "owner": wallet.owner,
            "pin": wallet.pin,
            "balance": wallet.balance,
            "transactions": wallet.transactions,
            "wrong_pin_attempts": wallet.wrong_pin_attempts,
            "locked": wallet.locked
        }

        wallet_data.append(wallet_details)

    with open("wallet_data.json", "w") as file:
        json.dump(wallet_data, file, indent=4)


def load_wallets():
    try:
        with open("wallet_data.json", "r") as file:
            wallet_data = json.load(file)

        for details in wallet_data:
            new_wallet = Wallet(
                details["owner"],
                details["pin"],
                details["balance"]
            )

            new_wallet.transactions = details["transactions"]
            new_wallet.wrong_pin_attempts = details["wrong_pin_attempts"]
            new_wallet.locked = details["locked"]

            wallets.append(new_wallet)

        print("Saved wallets loaded successfully!")

    except FileNotFoundError:
        print("No previous wallet records found.")

    except json.JSONDecodeError:
        print("The wallet data file is empty or damaged.")


def create_wallet():
    print("\n===== CREATE NEW WALLET =====")

    owner = input("Enter customer name: ").strip()
    pin = input("Create a 4-digit PIN: ")

    if not owner:
        print("Name cannot be empty.")
        return

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return

    for wallet in wallets:
        if wallet.owner.lower() == owner.lower():
            print("Customer already has a wallet.")
            return

    new_wallet = Wallet(owner, pin, 0)
    wallets.append(new_wallet)

    print("Wallet created successfully!")
    print("Welcome,", owner)


def login_wallet():
    print("\n===== CHECK WALLET BALANCE =====")

    owner = input("Enter your name: ").strip()

    for wallet in wallets:
        if wallet.owner.lower() == owner.lower():

            if wallet.locked:
                print("This wallet is locked.")
                return

            entered_pin = input("Enter your PIN: ")

            if wallet.verify_pin(entered_pin):
                wallet.display_wallet()

            return

    print("Wallet not found.")


def deposit_money():
    print("\n===== DEPOSIT MONEY =====")

    owner = input("Enter your name: ").strip()

    for wallet in wallets:
        if wallet.owner.lower() == owner.lower():

            if wallet.locked:
                print("This wallet is locked.")
                return

            entered_pin = input("Enter your PIN: ")

            if wallet.verify_pin(entered_pin):
                try:
                    amount = float(input("Enter amount to deposit: $"))
                    wallet.deposit(amount)

                except ValueError as error:
                    print("Error:", error)

            return

    print("Wallet not found.")


def withdraw_money():
    print("\n===== WITHDRAW MONEY =====")

    owner = input("Enter your name: ").strip()

    for wallet in wallets:
        if wallet.owner.lower() == owner.lower():

            if wallet.locked:
                print("This wallet is locked.")
                return

            entered_pin = input("Enter your PIN: ")

            if wallet.verify_pin(entered_pin):
                try:
                    amount = float(input("Enter amount to withdraw: $"))
                    wallet.withdraw(amount)

                except ValueError as error:
                    print("Error:", error)

            return

    print("Wallet not found.")


def transfer_money():
    print("\n===== SEND MONEY =====")

    sender_name = input("Enter your name: ").strip()
    recipient_name = input("Enter receiver's name: ").strip()

    sender_wallet = None
    recipient_wallet = None

    for wallet in wallets:
        if wallet.owner.lower() == sender_name.lower():
            sender_wallet = wallet

        if wallet.owner.lower() == recipient_name.lower():
            recipient_wallet = wallet

    if sender_wallet is None:
        print("Your wallet was not found.")
        return

    if recipient_wallet is None:
        print("Receiving wallet was not found.")
        return

    if sender_wallet.locked:
        print("Your wallet is locked.")
        return

    if recipient_wallet.locked:
        print("The receiving wallet is locked.")
        return

    entered_pin = input("Enter your PIN: ")

    if sender_wallet.verify_pin(entered_pin):
        try:
            amount = float(input("Enter amount to send: $"))
            sender_wallet.transfer(recipient_wallet, amount)

        except ValueError as error:
            print("Error:", error)


def view_transaction_history():
    print("\n===== VIEW TRANSACTION HISTORY =====")

    owner = input("Enter your name: ").strip()

    for wallet in wallets:
        if wallet.owner.lower() == owner.lower():

            if wallet.locked:
                print("This wallet is locked.")
                return

            entered_pin = input("Enter your PIN: ")

            if wallet.verify_pin(entered_pin):
                wallet.display_history()

            return

    print("Wallet not found.")


def main_menu():
    load_wallets()

    while True:
        print("\n===================================")
        print("     MOBILE MONEY WALLET SYSTEM")
        print("===================================")
        print("1. Create a new wallet")
        print("2. Check wallet balance")
        print("3. Deposit money")
        print("4. Withdraw money")
        print("5. Transfer money")
        print("6. View transaction history")
        print("7. Exit")
        print("===================================")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            create_wallet()

        elif choice == "2":
            login_wallet()

        elif choice == "3":
            deposit_money()

        elif choice == "4":
            withdraw_money()

        elif choice == "5":
            transfer_money()

        elif choice == "6":
            view_transaction_history()

        elif choice == "7":
            print("\nThank you for using our wallet system!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select a number from 1 to 7.")

        save_wallets()


main_menu()
