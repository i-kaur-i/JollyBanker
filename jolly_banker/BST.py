class BstNode:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val

    def insert(self, value):  # insert into BST
        if self.val:
            if value.id < self.val.id:  # if value is less then root/current value/account id
                if self.left is None:  # if left is none
                    self.left = BstNode(value)  # make left node filled with account
                else:
                    self.left.insert(value)  # else insert to the left side of tree

            elif value.id > self.val.id:  # check if value/id is greater then root/current account id. go to the right side
                if self.right is None:
                    self.right = BstNode(value)
                else:
                    self.right.insert(value)
        else:
            self.val = value

    def exists(self, value):  # check if account exists
        if value < self.val.id:  # if given id is less the root/current then go to left side
            if self.left is None:
                return False
            return self.left.exists(value)
        elif value > self.val.id:  # if its greater then goto right side
            if self.right is None:
                return False
            return self.right.exists(value)
        else:  # if neither then execute this
            return True

    def get_account(self, account):  # similart to exists function, only this time we return actual account instead of boolean
        if account < self.val.id:
            if self.left is None:
                return False
            return self.left.get_account(account)
        elif account > self.val.id:
            if self.right is None:
                return False
            return self.right.get_account(account)
        else:
            return self.val

    def get_all_accounts(self, accounts):
        if self.left:
            self.left.get_all_accounts(accounts)
        accounts.append(self.val)
        if self.right:
            self.right.get_all_accounts(accounts)