"""
This module works as client account Funds, each instance can have its name, balance, and most importantly
it saves all of its transaction history.
"""


class Fund:
    def __init__(self, name):
        self.balance = 0
        self.fund_name = name
        self.fund_history = []

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def get_balance(self):
        return self.balance

    def get_name(self):
        return self.fund_name

    def set_history(self, history):
        self.fund_history.append(history)  # append passed history to this list

    def get_history(self):
        return self.fund_history
