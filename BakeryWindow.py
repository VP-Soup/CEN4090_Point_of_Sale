from tkinter import *
import tkinter
import tkinter as tk
from functools import partial
from tkinter import ttk
import sqlite3

import DataAccess
import ViewDatabase,Transaction

# Bakery GUI window

class Bakery:

    def __init__(self, root):
        self.root = root
        #self.root.geometry('655x525+600+200')
        self.root.title('Bakery')
        self.create_main_window()

    def create_button_frame(container):
        frame = ttk.Frame(container)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame['borderwidth'] = 5
        frame['relief'] = 'raised'
        return frame

    def create_main_window(self):
        # root = Tk()
        # root.title = "POINT OF SALE"
        self.root.geometry = ('1920x1080')
        self.root.resizable(0, 0)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        main_frame = create_checkout_frame(self.root)
        button_frame = create_checkout_frame(self.root).grid(row=0, column=0)
        appName = ttk.Label(button_frame, text="CEN4020 Point Of Sale Application", font='roboto 20 bold')
        appName.grid(row=0, column=0, columnspan=3, sticky='nw')

        receipt_frame = create_checkout_frame(self.root)
        receipt_frame.grid(column=4, row=0)

        receipt = ItemWindow(receipt_frame)
        receipt.grid(row=0, rowspan=2, column=10, columnspan=10, sticky='n')

        product_Data = DataAccess.listAllProducts()  # get the names and prices from the product table
        n = len(product_Data)  # get the length
        i = 0  # associate names and prices to the buttons
        j = 1

        for productID, name, quan, cost, price, cat in product_Data:
            # print("Product ID: %s Names: %s and Price: %s and Quantity: %s",productID,name,price,quan)
            # MyButton(frame, 50,250,text=name, command=partial(print, price,cat)).grid(column=i, row=j+1, sticky="n,e,s,w", ipadx = 20, ipady = 20)
            # MyButton(frame, 50, 250, text=name, command=lambda name=name, price=price :add_item(name,price)).grid(column=i, row=j + 1, sticky="n,e,s,w",ipadx=20, ipady=20)
            MyButton(button_frame, 50, 250, text=name,
                     command=lambda name=name, price=price: ItemWindow.add_item(receipt, name, price)).grid(
                column=i, row=j + 1, sticky="n,e,s,w", ipadx=20, ipady=20)
            if i == 2:
                i = 0
                j += 1
            else:
                i += 1


class ItemWindow(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)
        self.text_box1 = tk.Text(self,width = 25, wrap=None, bg='white', font='roboto 24 bold')
        self.text_box1.grid(row=0, column=0, sticky='nsew')

        self.text_box2 = tk.Text(self, width = 10, wrap=None, bg='white', font='roboto 24 bold')
        self.text_box2.grid(row=0, column=1, sticky='nsew')

        self.scroller1 = tk.Scrollbar(self, command=self.text_box1.yview, orient='vertical')
        self.scroller2 = tk.Scrollbar(self, command=self.text_box2.yview, orient='vertical')
        self.text_box1.configure(yscrollcommand=self.scroller1.set)
        self.text_box2.configure(yscrollcommand=self.scroller1.set)
        self.scroller1.grid(row=0, column=1, sticky='nse')
        self.index = 0
        self.total = 0


    def add_item(self, name, price):
        newline = "\n"
        spacing = "                 $ "
        self.text_box1.insert('end',name)
        self.text_box1.insert('end', newline)
        self.text_box2.insert('end', price)
        self.text_box2.insert('end', newline)
        self.index += 1
        print("index = ",self.index)


class MyButton(ttk.Frame): #found at stackoverflow.com https://stackoverflow.com/questions/9927386/changing-ttk-button-height-in-python   (edited Apr 1 '16 at 6:49 - Pedru)
    def __init__(self,parent,height=None,width=None,text="",command=None,style=None, price = " "):
        ttk.Frame.__init__(self,parent,height=height,width=width,style="MyButton.TFrame")
        self.pack_propagate(0)
        self.price = price
        self._btn=ttk.Button(self, text=text,command=command,style=style)
        self._btn.pack(fill=tkinter.BOTH, expand=1)

def create_checkout_frame(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0,weight = 1)
    frame.columnconfigure(1,weight = 3)
    frame['borderwidth'] =5
    frame['relief'] = 'raised'
    # ttk.Label(frame, text = "CEN4020 Point Of Sale Application", font ='roboto 20 bold').grid(column = 0,columnspan = 2, row=0,sticky='nw')
    # for widget in frame.winfo_children():
    #     widget.grid(padx = 0, pady=0)
    return frame


    # root.mainloop()


