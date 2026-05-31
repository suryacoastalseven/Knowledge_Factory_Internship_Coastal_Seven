# 01_classes_objects.py

class BankAccount:
    # __init__ అనేది Constructor. ఆబ్జెక్ట్ క్రియేట్ అయినప్పుడు ముందు ఇది రన్ అవుతుంది.
    def __init__(self, account_holder: str, initial_balance: float):
        self.account_holder = account_holder
        # వేరియబుల్ ముందు రెండు అండర్ స్కోర్లు (__) పెడితే అది ప్రైవేట్ (Encapsulation)
        self.__balance = initial_balance 

    # డబ్బాలు డిపాజిట్ చేయడానికి ఒక పద్ధతి (Method)
    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ${amount}. New balance: ${self.__balance}")
        else:
            print("Invalid deposit amount.")

    # బ్యాలెన్స్ తెలుసుకోవడానికి (బయట వాళ్ళు డైరెక్ట్ గా బ్యాలెన్స్ మార్చకుండా సెక్యూరిటీ)
    def get_balance(self):
        return self.__balance

# Object Creation (ఇక్కడే అసలు మేజిక్ జరుగుతుంది)
print("--- OOP Basics: Encapsulation ---")
my_account = BankAccount(account_holder="Surya", initial_balance=1000)

print(f"Account Holder: {my_account.account_holder}")
my_account.deposit(500)
print(f"Secure Balance Check: ${my_account.get_balance()}")

# డైరెక్ట్ గా బ్యాలెన్స్ హ్యాక్ చేయాలని చూస్తే (my_account.__balance) ఎర్రర్ వస్తుంది. అదే OOP పవర్!