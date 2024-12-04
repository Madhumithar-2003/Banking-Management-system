import mysql.connector
import time
import datetime
from abc import ABC, abstractmethod  # Import abstract base classes

# Database connection setup
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql@123",
    database="banking"
)
bank_name = "Indian Bank"

# Abstract base class for account actions
class AbstractAccount(ABC):
    def _init_(self, account_no):
        self.account_no = account_no

    @abstractmethod
    def create_account(self, name, phone_no, aadhar_no, address, DOB):
        pass

    @abstractmethod
    def check_balance(self):
        pass

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def update_details(self, column_name, new_value):
        pass


# Derived class for a general bank account
class BankAccount(AbstractAccount):
    def __init__(self, account_no): 
        super()._init_(account_no)

    def create_account(self, name, phone_no, aadhar_no, address, DOB):
        cursor = mydb.cursor()
        sql = "INSERT INTO user_details (name, phone_no, aadhar_no, address, DOB, account_no, balance) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (name, phone_no, aadhar_no, address, DOB, self.account_no, 0.0)
        cursor.execute(sql, values)
        mydb.commit()
        print(f"{name}, your account was created successfully!")
        print(f"Your account number is {self.account_no}")
        cursor.close()

    def check_balance(self):
        cursor = mydb.cursor()
        sql = "SELECT balance FROM user_details WHERE account_no = %s"
        cursor.execute(sql, (self.account_no,))
        result = cursor.fetchone()
        if result:
            print(f"Your current balance is: {result[0]}")
        else:
            print("Account not found.")
        cursor.close()

    def deposit(self, amount):
        cursor = mydb.cursor()
        sql = "UPDATE user_details SET balance = balance + %s WHERE account_no = %s"
        values = (amount, self.account_no)
        cursor.execute(sql, values)
        mydb.commit()
        print(f"{amount} was deposited successfully!")
        print(datetime.datetime.now())
        cursor.close()

    def withdraw(self, amount):
        cursor = mydb.cursor()
        cursor.execute("SELECT balance FROM user_details WHERE account_no = %s", (self.account_no,))
        result = cursor.fetchone()
        if result:
            current_balance = result[0]
            if current_balance >= amount:
                new_balance = float(current_balance) - amount
                cursor.execute("UPDATE user_details SET balance = %s WHERE account_no = %s", (new_balance, self.account_no))
                mydb.commit()
                print(f"{amount} withdrawn successfully!")
            else:
                print("Insufficient balance!")
        else:
            print("Account not found.")
        cursor.close()

    def update_details(self, column_name, new_value):
        cursor = mydb.cursor()
        sql = f"UPDATE user_details SET {column_name} = %s WHERE account_no = %s"
        values = (new_value, self.account_no)
        cursor.execute(sql, values)
        mydb.commit()
        print(f"Updated {column_name} for account {self.account_no} successfully!")
        cursor.close()


# Derived class for specific account type (e.g., Savings Account)
class SavingsAccount(BankAccount):
    def withdraw(self, amount):
        print("Savings Account: Withdrawal limit check")
        super().withdraw(amount)


# Derived class for specific account type (e.g., Current Account)
class CurrentAccount(BankAccount):
    def withdraw(self, amount):
        print("Current Account: No withdrawal limit")
        super().withdraw(amount)


# Main function to drive the program
def main():
    while True:
        print(f"\nWelcome to {bank_name}")
        time.sleep(0.5)
        print("\n1. Create Account\n2. Deposit Amount\n3. Withdraw Amount\n4. Check Balance\n5. Update Details\n6. Exit")
        choice = int(input("Enter your choice (1-6): "))

        if choice == 1:
            name = input("Enter your name: ")
            phone_no = int(input("Enter your mobile no: "))
            aadhar_no = int(input("Enter your aadhar no: "))
            address = input("Enter your address: ")
            DOB = input("Enter your DOB (yyyy-mm-dd): ")
            account_no = input("Enter your account no: ")

            account = BankAccount(account_no)
            account.create_account(name, phone_no, aadhar_no, address, DOB)

        elif choice == 2:
            account_no = input("Enter your account no: ")
            amount = float(input("Enter deposit amount: "))

            account = BankAccount(account_no)
            account.deposit(amount)

        elif choice == 3:
            account_no = input("Enter your account no: ")
            amount = float(input("Enter withdrawal amount: "))
            account_type = input("Enter account type (savings/current)")

            if account_type == "savings":
                account = SavingsAccount(account_no)
            elif account_type == "current":
                account = CurrentAccount(account_no)
            else:
                print("Invalid account type!")
                continue

            account.withdraw(amount)

        elif choice == 4:
            account_no = input("Enter your account no: ")

            account = BankAccount(account_no)
            account.check_balance()

        elif choice == 5:
            account_no = input("Enter your account no: ")
            column_name = input("Enter the detail to be updated (e.g., name, phone_no, aadhar_no, DOB, address): ")
            new_value = input("Enter the new value: ")

            account = BankAccount(account_no)
            account.update_details(column_name, new_value)

        elif choice == 6:
            print("Thank you for using the Banking system.\nHave a great day!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
