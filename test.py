from tkinter import *
from functools import partial
from tkinter import ttk

class LineItem:
    def __init__(self, tid, itemID):
        # call DAL to get values to populate these lines properly
        self.itemID = itemID
        self.quantity = 1
        self.price = 0.0
        self.nameID = itemID
        self.lineID = 0
        self.tid = tid

    def add_quantity(self, itemID):
        if self.itemID == itemID:
            self.quantity += 1
            self.price += 1 #replace with some way to get the original value of 1 item * added quantity
            return True
        else:
            return False

    def print_self(self):
        print(self.nameID, "\tQuantity: ", self.quantity, "\tPrice: ", self.price)


class Transaction:
    def __init__(self):
        self.lines = []
        self.tid = 0
        self.eid = ""
        self.timestamp = ""
        self.pre_tax = 0.0
        self.discount = 0.0
        self.tax = 1.10
        self.final_cost = 0.0
        self.cash_method = False
        self.cash_received = 0.0
        self.change_returned = 0.0
        self.transaction_status = 0

    def add_item(self, itemID):
        for line in self.lines:
            if line.add_quantity(itemID):
                return
        new_line = LineItem(self.tid, itemID)
        self.lines.append(new_line)

    def print_receipt(self):
        for line in self.lines:
            line.print_self()


def end():
    exit(0)


def main():
    transaction = Transaction()

    root = Tk()
    root.title("Test")
    frame = Frame(root)
    frame.grid(column=0, row=0)

    # some call to populate an array full of info
    items = [("name", "price"), ("name1", "price1"), ]

    i = j = 1
    for item in items:
        ttk.Button(frame, text=item[0], command=partial(transaction.add_item, item[0])).grid(column=i, row=j,
                                                                                             sticky="n,e,s,w")
        if i == 3:
            i = 1
            j += 1
        else:
            i += 1

    ttk.Button(frame,text="Receipt",command=partial(transaction.print_receipt)).grid(column=i, row=j, sticky="n,e,s,w")

    if i == 3:
        i = 1
        j += 1
    else:
        i += 1

    ttk.Button(frame, text="Exit", command=partial(exit, 0)).grid(column=i, row=j,sticky="n,e,s,w")

    root.minsize(width=270, height=270)
    root.mainloop()


if __name__ == "__main__":
    main()
