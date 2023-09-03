from Fund import Fund


class Account:
    def __init__(self, id, first_name, last_name, fund_names):
        self.id = id
        self.fname = first_name
        self.lname = last_name
        self.funds = []
        self.all_history = {}
        for i in range(len(fund_names)):
            self.funds.append(Fund(fund_names[i]))

    def deposit(self, fund, amount):  # deposit give amount to given fund number e.g 0 for Money Market
        if 0 <= fund < 10:  # check if fund is between 0 and 9 inclusive, if not then no such fund exists. else execute below

            history = "D " + str(self.id) + str(fund) + " " + str(amount)  # make a transaction record
            self.funds[fund].deposit(amount)  # deposite specific amount to that exact fund balance
            self.funds[fund].set_history(history)  # add record/history of transaction to that fund
            return None
        else:
            return "No such fund type for this account."

    def withdraw(self, fund, amount):  # withdraw given amount from client funds
        if 0 <= fund < 10:  # check if fund is between 0 and 10 inclusive.
            if fund in [0, 1, 2, 3]:  # check if fund is between 0 and 3 inclusive, because these are 2 pairs of account that can be used to compensate for each other incase of low balance in other fund
                fund_dict = {0: 1, 1: 0, 2: 3, 3: 2}  # if with drawing from given fund is 0 then it can withdraw from fund 1 if needed be.
                alternate_fund = fund_dict.get(fund)
                if self.funds[fund].get_balance() < amount:  # if fund amount is less the withdrawlamount
                    if self.funds[alternate_fund].get_balance() + self.funds[fund].get_balance() >= amount:  # check if the alternative fund account have enough funds to compensate for it.

                        cover_amount = amount - self.funds[fund].get_balance()  # first get cover_amount , it is the amount needed from alternate fund to compensate for our current fund account
                        self.funds[alternate_fund].withdraw(cover_amount)  #  withdraw that amount from alternate fund
                        self.funds[fund].withdraw(amount-cover_amount)  # with draw remaining amount from current fund ( means it will leave current fund with 0 balance)
                        history = "W " + str(self.id) + str(fund) + " " + str(amount)  # save history/record
                        self.funds[fund].set_history(history)
                        return True
                    else:
                        return False
                else:
                    self.funds[fund].withdraw(amount)  # if withdrawl amount is equal to fund balance then simply withdraw
                    history = "W " + str(self.id) + str(fund) + " " + str(amount)
                    self.funds[fund].set_history(history)
                    return True
            else:
                if self.funds[fund].get_balance() >= amount:
                    self.funds[fund].withdraw(amount)
                    history = "W " + str(self.id) + str(fund) + " " + str(amount)
                    self.funds[fund].set_history(history)
                    return True
                else:
                    return False
        else:
            return False

    def transfer_funds(self, fund, amount, destination, des_fund):
        if isinstance(destination, int):  # check if destination given is account or id
            if 0<= des_fund < 10:  # if destination is id check if fund num is between 0 and 9 inclusive
                self.withdraw(fund, amount)  # withdraw amount from given account
                self.deposit(des_fund, amount)  # transfer amount to the other fund
                history = "T " + str(self.id) + str(fund) + " " + str(amount) +' ' + str(destination) + str(des_fund)  # record history
                self.funds[fund].set_history(history)
                return True
            else:
                return False
        else:
            if self.withdraw(fund, amount):  # if destination is another account
                history = "T " + str(self.id) + str(fund) + " " + str(amount) + ' ' + str(destination) + str(des_fund)  #
                self.funds[fund].set_history(history)
                return destination.deposit(des_fund, amount)  # deposit funds there
            else:
                return 'Transfer of funds from id ' + str(id) + " to id " + str(destination) + " has Failed due to insufficient amount"

    def display_all_history(self):

        for i in range(len(self.funds)):
            self.all_history[self.get_name()] = 'Transaction History for ' + self.get_name() + " by fund."
            fund = self.funds[i]
            if fund.get_history():
                history = fund.get_history()
                fund_name_amount = fund.get_name() + ": $" + str(fund.get_balance())
                for ii in range(len(history)):
                    if fund_name_amount not in self.all_history.keys():
                        self.all_history[fund_name_amount] = [history[ii]]
                    else:
                        self.all_history[fund_name_amount].append(history[ii])

        return self.all_history

    def display_fund_history(self, fund):
        fund_history = {}
        fund_history[self.get_name()] = 'Transaction History for ' + self.get_name() + " by " + self.funds[fund].get_name()
        fund = self.funds[fund]
        fund_name_amount = fund.get_name() + ": $" + str(fund.get_balance())
        history = fund.get_history()
        for i in range(len(history)):
            if fund_name_amount not in fund_history.keys():
                fund_history[fund_name_amount] = [history[i]]
            else:
                fund_history[fund_name_amount].append(history[i])
        return fund_history

    def get_id(self):
        return self.id

    def get_name(self):
        return self.fname + " " + self.lname

    def get_balance(self, fund):
        return self.funds[fund].get_balance()