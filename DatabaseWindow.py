from tkinter import *
import tkinter
import tkinter as tk
from functools import partial
from tkinter import ttk
import sqlite3
import sys
import DataAccess
import ViewDatabase,Transaction

# Database GUI window for entering products into the database




class DatabaseWindow:
    global count
    count=0
    def __init__(self, root):
        self.root = root
        self.root.title('Database Entry')
        self.root.geometry = ('1920x1080')

        #CREATE A CONNECTION TO THE DATABASE
        conn=sqlite3.connect('BakeryDatabase.db')
        c=conn.cursor()

        db_style=ttk.Style()
        db_style.theme_use('default')
        db_style.configure('db_Treeview',
                           background="#eae1df",
                           foreground='black',
                           rowheight=30,
                           fieldbackground="#eae1df",
                           font=('Helvetica',30))

        db_style.map('db_Treeview',
                     background=[('selected','#347083')])
        db_frame=Frame(root)
        db_frame.pack(pady=10)

        db_scroll=Scrollbar(db_frame)
        db_scroll.pack(side=RIGHT, fill=Y)

        db_view=ttk.Treeview(db_frame,yscrollcommand=db_scroll.set,selectmode="extended")
        db_view.pack()

        db_scroll.config(command=db_view.yview)

        #CREATE A COLUMN HEADER FOR THE DATABASE AND FORMAT
        db_view['columns']=("ID","NAME","QUANTITY","PRICE","COST","CATEGORY")
        db_view.column("#0",width=0,stretch=NO)
        db_view.column("ID",anchor=W,width=100)
        db_view.column("NAME", anchor=CENTER,width=150)
        db_view.column("QUANTITY", anchor=CENTER,width=150)
        db_view.column("PRICE", anchor=CENTER,width=150)
        db_view.column("COST", anchor=CENTER,width=150)
        db_view.column("CATEGORY", anchor=CENTER, width=150)

        #DB VIEW COLUMN HEADINGS
        db_view.heading("#0",text="",anchor=W)
        db_view.heading("ID", text="ID", anchor=W)
        db_view.heading("NAME", text="NAME", anchor=CENTER)
        db_view.heading("QUANTITY", text="QUANTITY", anchor=CENTER)
        db_view.heading("PRICE", text="PRICE", anchor=CENTER)
        db_view.heading("COST", text="COST", anchor=CENTER)
        db_view.heading("CATEGORY", text="CATEGORY", anchor=CENTER)

        db_view.tag_configure('oddrow',background='#eae1df')
        db_view.tag_configure('evenrow',background='#f1b0a2')



        db_entry=DataAccess.listAllProducts()
        for entry in db_entry:
            global count
            if count%2==0:
                db_view.insert(parent='',index='end',iid=count,text='', values=(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5]),tags=('evenrow',))
            else:
                db_view.insert(parent='', index='end', iid=count, text='', values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]),tags=('oddrow',))
            count+=1

        #CREATE AN ENTRY FORM INTO THE PRODUCT DATABASE
        db_entry_frame=LabelFrame(root,text="Database Entry")
        db_entry_frame.pack(fill="x",expand=Y,padx=10,pady=20)

        product_ID_label = Label(db_entry_frame,text="PRODUCT ID")
        product_ID_label.grid(row=0, column=0, padx=10, pady=10)

        product_ID_entry=Entry(db_entry_frame,width=30)
        product_ID_entry.grid(row=0, column=1, padx=10, pady=10)
        #
        db_name_label=Label(db_entry_frame,text="NAME")
        db_name_label.grid(row=0,column=2, padx=10, pady=10)
        db_name_entry=Entry(db_entry_frame,width=30)
        db_name_entry.grid(row=0, column=3, padx=10, pady=10)
        #
        db_quan_label = Label(db_entry_frame, text="QUANTITY")
        db_quan_label.grid(row=1, column=0, padx=10, pady=10)
        db_quan_entry = Entry(db_entry_frame, width=30)
        db_quan_entry.grid(row=1, column=1, padx=10, pady=10)
        #
        db_sellPrice_label = Label(db_entry_frame, text="SELLING PRICE")
        db_sellPrice_label.grid(row=1, column=2, padx=10, pady=10)
        db_sellPrice_entry = Entry(db_entry_frame, width=30)
        db_sellPrice_entry.grid(row=1, column=3, padx=10, pady=10)
        #
        db_cost_label = Label(db_entry_frame, text="COST")
        db_cost_label.grid(row=2, column=0, padx=10, pady=10)
        db_cost_entry = Entry(db_entry_frame, width=30)
        db_cost_entry.grid(row=2, column=1, padx=10, pady=10)
        #
        db_category_label = Label(db_entry_frame, text="CATEGORY")
        db_category_label.grid(row=2, column=2, padx=10, pady=10)
        db_category_entry = Entry(db_entry_frame, width=30)
        db_category_entry.grid(row=2, column=3, padx=10, pady=10)

        def select_record(x):
            product_ID_entry.delete(0,END)
            db_name_entry.delete(0,END)
            db_sellPrice_entry.delete(0,END)
            db_quan_entry.delete(0, END)
            db_cost_entry.delete(0, END)
            db_category_entry.delete(0, END)

            selected_record=db_view.focus()
            selected_values=db_view.item(selected_record,'values')

            product_ID_entry.insert(0, selected_values[0])
            db_name_entry.insert(0, selected_values[1])
            db_sellPrice_entry.insert(0, selected_values[2])
            db_quan_entry.insert(0, selected_values[3])
            db_cost_entry.insert(0, selected_values[4])
            db_category_entry.insert(0, selected_values[5])

        db_view.bind("<ButtonRelease-1>", select_record)

        def clear_record():
            product_ID_entry.delete(0,END)
            db_name_entry.delete(0,END)
            db_sellPrice_entry.delete(0,END)
            db_quan_entry.delete(0, END)
            db_cost_entry.delete(0, END)
            db_category_entry.delete(0, END)

        #CREATE A NEW FRAME TO ADD THE RECORD ENTRY AND DELETE BUTTONS
        db_button_frame = LabelFrame(root, text="Database Records Controls")
        db_button_frame.pack(fill="x", expand=Y, padx=10, pady=20)

        update_button=Button(db_button_frame,text="UPDATE RECORD")
        update_button.grid(row=0,column=0,padx=10,pady=10, ipadx=10, ipady=10,sticky=N)

        add_records_button = Button(db_button_frame, text="NEW RECORD")
        add_records_button.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        remove_record_button = Button(db_button_frame, text="REMOVE RECORD")
        remove_record_button.grid(row=0, column=2, padx=10, pady=10, ipadx=10, ipady=10)

        remove_all_button = Button(db_button_frame, text="REMOVE ALL RECORDS")
        remove_all_button.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        move_up_button = Button(db_button_frame, text="MOVE RECORD UP")
        move_up_button.grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        move_down_button=Button(db_button_frame,text="MOVE RECORD DOWN")
        move_down_button.grid(row=1,column=2,padx=10,pady=10, ipadx=10, ipady=10)

        select_button = Button(db_button_frame, text="CLEAR RECORD",command=clear_record)
        select_button.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10)


        root.mainloop()