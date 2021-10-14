from tkinter import *
from tkinter import ttk
from functools import partial
from Transaction import Transaction


def main():
    transaction = Transaction()

    root = Tk()
    root.title('test')

    frame = ttk.Frame(root, padding='8')
    frame.grid(column=0, row=0)

    items = [("name", "price"), ("name1", "price1")]

    i = 1
    j = 1

    for item in items:
        ttk.Button(frame, text=item[0], command=partial(transaction.add_item, item[0])).grid(column=i, row=j, sticky=W)

        if i == 3:
            i = 1
            j += 1
        else:
            i += 1

    ttk.Button(frame, text="Receipt", command=partial(transaction.print_receipt)).grid(column=i, row=j, sticky=W)

    if i == 3:
        i = 1
        j += 1
    else:
        i += 1

    ttk.Button(frame, text="Exit", command=partial(transaction.print_receipt)).grid(column=i, row=j, sticky=W)

    root.mainloop()

    return


if __name__ == "__main__":
    main()