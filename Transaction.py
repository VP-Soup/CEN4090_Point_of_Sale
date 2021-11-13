# defines LineItem and Transaction classes

from DataAccess import *


# class represents one line of receipt
class LineItem:
    # initialize LineItem with tid of Transaction, and item
    def __init__(self, tid, itemID, quantity):
        # call DAL to get values to populate these lines properly
        self.itemID = itemID
        self.quantity = quantity
        self.price = getProductCostFromID(itemID)
        self.nameID = getProductNameFromID(itemID) #changed the the fn call instead of assigning itemID -Rob
        self.tid = tid

    # method to increment quantity by an amount
    # should query DB to adjust price appropriately
    # returns self.quantity upon success, which will be used to determine empty
    # return -1 if called with wrong itemID or inappropriate adjustment amount
    def increment_quantity(self, itemID, amount):
        if self.itemID == itemID and amount <= self.quantity:
            self.quantity += amount
            self.price = getProductCostFromID(itemID) * self.quantity
            return self
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


# class represents the total transaction
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
        self.transaction_status = 0  # 0 : in progress; 1 : complete; -1 : paused;

    # method to add a new item or increment an existing item
    def increment_item(self, itemID, amount):
        for line in self.lines:
            if line.increment_quantity(itemID, amount) != -1:
                return
        self.lines.append(LineItem(self.tid, itemID, amount))
        return

    # method to entirely remove an item from the transaction
    # Rob-added the index and changed to del self.lines[index]
    def remove_item(self, itemID):
        index=0
        for line in self.lines:
            if line.get_itemID() == itemID:
                del self.lines[index]
                return
            index+=1
        return print("Error: No such item in transaction.")

    # replace with method to connect to GUI Receipt area or File output
    def print_receipt(self):
        self.update_price()
        if self.tid != -1:
            print("RECEIPT:")
            for line in self.lines:
                line.print_self()
        else:
            print("Error: Transaction not submitted to DB yet")

    # method to pause transaction
    def pause_transaction(self):
        # insert into DB
        self.transaction_status = -1
        # Call to GUI to store this transaction?

    # method to update price related attributes
    def update_price(self):
        running_total = 0
        for line in self.lines:
            running_total += line.get_price()
        self.pre_tax = running_total
        self.final_cost = running_total*(1-self.discount)*self.tax

    # method to clear transaction of all values
    def clear_transaction(self):
        for line in self.lines:
            del line
        self.update_price()

    # called at the end of the transaction
    def finalize_transaction(self, cash_status, cash_amount):
        self.update_price()
        self.cash_method = cash_status
        self.cash_received = cash_amount
        self.change_returned = self.cash_received - self.final_cost
        self.transaction_status = 1
        # insert into DB
        self.print_receipt()
