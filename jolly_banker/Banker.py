from Queue import Queue
from Account import Account
from BST import BstNode


def read_input(filename):
    queue = Queue()
    with open(filename) as file:
        for line in file.readlines():
            transaction = line.strip('\n')
            queue.insert(transaction)
    return queue


def write_to_file(messages, root, fund_names):

    with open("BankTransOut.txt", 'w') as file:
        for message in messages:
            if message is None:
                pass
            else:
                if isinstance(message, dict):
                    for key, items in message.items():
                        if isinstance(items, str):
                            file.write('\n\n')
                            file.write(items + "\n")
                        else:
                            file.write(key + "\n")
                            for item in items:
                                file.write(" " + item + "\n")
                else:
                    file.write(message + "\n")

        accounts = []
        root.get_all_accounts(accounts)
        file.write("\nProcessing Done. Final Balances\n")
        for account in accounts:
            file.write('\n')
            file.write(account.get_name() + " Account ID: " + str(account.get_id()) + "\n")
            for i in range(len(fund_names)):
                file.write("    " + fund_names[i] + ": $"+ str(account.get_balance(i)) + "\n")



def main():
    queue = read_input("BankTransIn.txt")
    fund_names = ['Money Market', 'Prime Money Market', 'Long-Term Bond',
                  'Short-Term Bond', '500 Index Fund', 'Capital Value Fund',
                  'Growth Equity Fund', 'Growth Index Fund', 'Value Fund',
                  'Value Stock Index']
    root = None
    messages = []

    for _ in range(queue.get_size()):
        transaction = queue.pop()  # pop top transaction from queue
        transaction = transaction.split(' ')  # split transaction by space
        # account = None
        if transaction[0] == 'O':  # check if transaction is O
            account = Account(int(transaction[3]), transaction[1], transaction[2], fund_names)  # create account
            if root is None:  # if BST is yet not created, create one
                root = BstNode(account)
            else:
                if root.exists(int(transaction[3])):  # if id exists record current error
                    messages.append("ERROR: Account " + transaction[3] + " is already open. Transaction refused.")
                root.insert(account)  #  insert accunt to BST

        elif transaction[0] == 'D':  # for Deposit transaction
            amount = float(transaction[2])
            fund = int(transaction[1][-1])
            id = int(transaction[1][:-1])

            if root.exists(id):  # if account is exists. all our accounts are in BST

                account = root.get_account(id)  # get that account
                messages.append(account.deposit(fund, amount))  # deposit amount
            else:
                messages.append("ERROR: Account No " + str(id) + " not found. Refused Transaction")

        elif transaction[0] == 'W':  # for withdrawl transaction
            amount = float(transaction[2])
            fund = int(transaction[1][-1])
            id = int(transaction[1][:-1])

            if root.exists(id):
                account = root.get_account(id)
                response = account.withdraw(fund, amount)  # withdarw amount
                if not response:  # if with draw amount is False then save this message
                    messages.append("ERROR: Not enough funds to withdraw " + str(amount) + " from " + account.get_name()
                                          + " " + fund_names[fund])
            else:
                messages.append("ERROR: Account No " + str(id) + " not found. Refused Transaction")

        elif transaction[0] == 'T':
            id1 = int(transaction[1][:-1])
            id2 = int(transaction[3][:-1])
            fund1 = int(transaction[1][-1])
            fund2 = int(transaction[3][-1])
            amount = float(transaction[2])

            if root.exists(id1):
                account1 = root.get_account(id1)
                if id2 == id1:
                    response = account1.transfer_funds(fund1, amount, id2, fund2)

                    if isinstance(response, str):
                        messages.append(response)
                elif root.exists(id2):
                    account2 = root.get_account(id2)
                    response = account1.transfer_funds(fund1, amount, account2, fund2)
                    if isinstance(response, str):
                        messages.append(response)

                else:
                    messages.append("ERROR: Destination account " + str(id2) + " doesn't exists")

        elif transaction[0] == 'H':

            if root.exists(int(transaction[1][:4])):
                account = root.get_account(int(transaction[1][:4]))
                if len(transaction[1]) == 4:
                    messages.append(account.display_all_history())
                else:
                    messages.append(account.display_fund_history(int(transaction[1][-1])))
            else:
                messages.append('ERROR: No such account with id ' + str(transaction[1][:4]) + ' exists')

    write_to_file(messages, root, fund_names)


main()
