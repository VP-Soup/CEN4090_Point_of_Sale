# defines LineItem and Transaction classes

from DataAccess import *


class LineItem:
    # initialize LineItem with tid of Transaction, and item
    def __init__(self, tid, itemID, quantity):
        # call DAL to get values to populate these lines properly
        self.itemID = itemID
        self.quantity = quantity
        self.price = getProductCostFromID(itemID)
        self.nameID = itemID
        self.tid = tid

    # method to increment quantity by an amount
    # should query DB to adjust price appropriately
    # returns self.quantity upon success, which will be used to determine empty
    # return -1 if called with wrong itemID or inappropriate adjustment amount
    def increment_quantity(self, itemID, amount):
        if self.itemID == itemID and amount <= self.quantity:
            self.quantity += amount
            self.price += getProductCostFromID(itemID) * amount
            return self.quantity
        else:
            return -1

    # reduce price to discount
    def apply_discount(self, discount):
        self.price *= 1 - discount

    def print_self(self):
        print(self.nameID, "\tQuantity: ", self.quantity, "\tPrice: ", self.price)

    def get_itemID(self):
        return self.itemID

    def get_price(self):
        return self.price


class Transaction:
    def __init__(self, eid):
        self.lines = []  # list of all line items
        self.tid = -1  # replace with insert to DB which should return real TID
        self.eid = eid  # employee id of employee handling transaction
        self.timestamp = ""  # timestamp of transaction
        self.pre_tax = 0.0  # transaction total pre-tax
        self.discount = 0.0  # any global discount
        self.tax = 1.10  # global tax - potentially replace with DAL call to state tax
        self.final_cost = 0.0  # final tax value
        self.cash_method = False  # bool for if transaction paid in cash or not
        self.cash_received = 0.0  # cash tendered
        self.change_returned = 0.0  # excess in cash tendered
        self.transaction_status = 0  # 0 : in progress; 1 : complete; -1 : terminated; 2: paused

    # method to add a new item or increment an existing item
    def increment_item(self, itemID, amount):
        for line in self.lines:
            if line.increment_quantity(itemID, amount) != -1:
                return
        self.lines.append(LineItem(self.tid, itemID, amount))

    # method to entirely remove an item from the transaction
    def remove_item(self, itemID):
        for line in self.lines:
            if line.get_itemID == itemID:
                del line
                return
        return print("Error: No such item in transaction.")

    # replace with method to connect to GUI Receipt area or File output
    def print_receipt(self):
        if self.tid != -1:
            print("RECEIPT:")
            for line in self.lines:
                line.print_self()
        else:
            print("Error: Transaction not submitted to DB yet")

    def pause_transaction(self):
        # insert into DB
        self.transaction_status = 2
        # Call to GUI to store this transaction?

    def update_price(self):
        running_total = 0
        for line in self.lines:
            running_total += line.get_price()
        self.pre_tax = running_total
        self.final_cost = running_total*(1-self.discount)*self.tax

    def clear_transaction(self):
        for line in self.lines:
            del line
