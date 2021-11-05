##########################################################################################################
## Application Bakery Point of Sale - 3FPS                                                              ##
## Bakery Database GUI: interface with the products datatable for product addition, removal, etc        ##
##                      Main area is the treeview for the database records, followed by an area to      ##
##                      record new product information. The last section is for the sql commands to     ##
##                      edit the records in the database.                                               ##
## References: YouTube.com, Codemy.com, Stackoverflow.com, tutorialspoint.com, geeksforgeeks.org,       ##
##            pythonguides.com, anzeljg.github.io, & pythontutorial.net                                 ##
## Date: 06NOV21                                                                                        ##
##########################################################################################################

from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3

import BakeryButton, DataAccess,BakeryWindow,Charts,About


class DatabaseWindow:
    #GLOBAL COUNT VARIABLE FOR THE ROWS ODD/EVEN
    global count
    count=0

    def doNothing():
        pass

    # SHOW BAKERY WINDOW
    def showBakeryWindow(e):
        e.destroy()
        newRoot = Tk()
        application = BakeryWindow.Bakery(newRoot)
        newRoot.mainloop()

    # SHOW THE CHARTS WINDOW
    def showCharts(e):
        e.destroy()
        newRoot = Tk()
        application = Charts.Graph(newRoot)
        newRoot.mainloop()

    def __init__(self, root):
        #SET THE WINDOW DIMENSIONS
        root_width = 1900
        root_height = 1000
        button_width=175
        button_height=60
        self.root = root
        self.root.title('Database Entry')

        # CREATE A MENU BAR
        app_menu = Menu(self.root)

        # FILE MENU ITEMS; ONLY THE EXIT ACTUALLY DOES ANYTHING AT THE MOMENT
        file_menu = Menu(app_menu, tearoff=0)
        file_menu.add_command(label="New", )
        file_menu.add_command(label="Open", )
        file_menu.add_command(label="Save", )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.destroy)
        app_menu.add_cascade(label="File", menu=file_menu)

        # ADMINISTRATOR MENU OPTIONS
        # LOGIN SHOWS THE LOGIN WINDOW
        # LOGOUT WILL CLOSE THE OPEN WINDOW AND SHOW THE BAKERY WINDOW
        # CHARTS REQUIRES NO LOGIN, SHOWS THE CHART WINDOW
        admin_menu = Menu(app_menu, tearoff=0)
        admin_menu.add_command(label="Login", command=lambda: BakeryWindow.showLoginWindow(self.root))
        admin_menu.add_command(label="Logout", command=lambda: BakeryWindow.Bakery(self.root))
        admin_menu.add_separator()
        admin_menu.add_command(label="Charts", command= lambda: DatabaseWindow.showCharts(self.root))
        app_menu.add_cascade(label="Admin", menu=admin_menu)

        # HELP MENU OPTIONS
        # HAS THE ABOUT POPUP WINDOW THAT WILL LIST CODE AND TUTORIAL SOURCES
        help_menu = Menu(app_menu, tearoff=0)
        help_menu.add_command(label="Help", )
        help_menu.add_command(label="About",command=About.About)
        app_menu.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=app_menu)

        # GET THE DISPLAY WINDOW DIMENSIONS
        screen_width=root.winfo_screenwidth()
        screen_height=root.winfo_screenheight()

        # FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x=int(screen_width/2-root_width/2)
        window_center_y=int(screen_height/2-root_height/2)

        # SET THE ROOT WINDOW LOCATION ON THE DISPLAY
        root.geometry(f'{root_width}x{root_height}+{window_center_x}+{window_center_y}')
        canvas = tk.Canvas(master=self.root, width=root_width, height=root_height, bg='white')
        canvas.pack()
        canvas['highlightcolor']='white'

        # CREATE A CONNECTION TO THE DATABASE
        conn=sqlite3.connect('BakeryDatabase.db')

        # SET THE STYLE OF THE DATABASE ENTRY
        db_style=ttk.Style()
        db_style.configure('db.Treeview',
                           background="#eae1df",
                           foreground='black',
                           rowheight=50,
                           fieldbackground="#eae1df",
                           ipady=10,
                           font=('Times',20))
        db_style.configure('db.Treeview.Heading',
                                   font=('Times',22,'bold'))

        db_style.map('db.Treeview',
                     background=[('selected','#347083')])
        db_frame=ttk.Frame(canvas,height = root_height/2,width=root_width)
        db_frame['padding']=5
        db_frame['borderwidth']=0
        db_frame['relief']='sunken'
        db_frame.pack(expand=True)

        #ADD THE VERTICAL SCROLL BAR TO THE DATABASE ENTRY
        db_vert_scroll=Scrollbar(db_frame)
        db_vert_scroll.pack(side=RIGHT, fill=Y)

        # ADD THE HORIZONTAL SCROLL BAR TO THE DATABASE ENTRY
        db_horz_scroll = Scrollbar(db_frame,orient='horizontal')
        db_horz_scroll.pack(side=BOTTOM, fill='x')

        #SET THE DATABASE VIEW WITH SCROLL BARS VERT AND HORIZ.
        db_view=ttk.Treeview(db_frame,
                             style="db.Treeview",
                             xscrollcommand=db_horz_scroll.set,
                             yscrollcommand=db_vert_scroll.set,
                             selectmode="extended")#modes are 'browse','extended','none'
        db_view.pack()
        db_vert_scroll.config(command=db_view.yview)
        db_horz_scroll.config(command=db_view.xview)


        #CREATE COLUMN HEADERS FOR THE DATABASE AND FORMAT
        db_view['columns']=("ID","NAME","QUANTITY","PRICE","COST","CATEGORY")
        db_view.column("#0",
                       width=0,
                       stretch=NO)
        db_view.column("ID",
                       anchor=W,
                       #width=150, #HAVING A PRESET WIDTH CAUSED ISSUES
                       stretch=YES)
        db_view.column("NAME",
                       anchor=CENTER,
                       #width=150, #HAVING A PRESET WIDTH CAUSED ISSUES
                       stretch=YES)
        db_view.column("QUANTITY",
                       anchor=CENTER,
                       #width=150, #HAVING A PRESET WIDTH CAUSED ISSUES
                       stretch=YES)
        db_view.column("PRICE",
                       anchor=CENTER,
                       #width=150, #HAVING A PRESET WIDTH CAUSED ISSUES
                       stretch=YES)
        db_view.column("COST",
                       anchor=CENTER,
                       #width=150, #HAVING A PRESET WIDTH CAUSED ISSUES
                       stretch=YES)
        db_view.column("CATEGORY",
                       anchor=CENTER,
                       #width=150, #HAVING A PRESET WIDTH CAUSED ISSUES
                       stretch=YES)

        #DATABASE VIEW COLUMN HEADINGS, NAME AND LOCATION
        db_view.heading("#0",text="")
        db_view.heading("ID", text="ID", anchor=W)
        db_view.heading("NAME", text="NAME", anchor=CENTER)
        db_view.heading("QUANTITY", text="QUANTITY", anchor=CENTER)
        db_view.heading("PRICE", text="PRICE", anchor=CENTER)
        db_view.heading("COST", text="COST", anchor=CENTER)
        db_view.heading("CATEGORY", text="CATEGORY", anchor=CENTER)

        #SET ALTERNATING COLORS FOR THE DATABASE ENTRIES
        db_view.tag_configure('oddentry',background='#eae1df')
        db_view.tag_configure('evenentry',background='#f1b0a2')


        #SQL QUERY TO RETURN ALL THE PRODUCTS FROM THE DATABASE ADD ASSIGN COLORS TO THE ROWS
        db_entry=DataAccess.listAllProducts()
        for entry in db_entry:
            global count
            if count%2==0:
                db_view.insert(parent='',
                               index='end',
                               iid=count,
                               text='',
                               values=(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5]),tags=('evenentry',))
            else:
                db_view.insert(parent='',
                               index='end',
                               iid=count,
                               text='',
                               values=(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]),tags=('oddentry',))
            count+=1

        #ADD AN ENTRY FORM INTO THE PRODUCT DATABASE
        db_entry_frame=LabelFrame(canvas,text="Database Entry")
        #db_entry_frame['borderwidth']=0
        db_entry_frame.pack(fill="x",expand=Y,padx=20,pady=20)

        #ADD PRODUCT ID LABEL TO THE GRID
        product_ID_label = Label(db_entry_frame,text="PRODUCT ID",justify="right")
        product_ID_label.grid(row=0, column=0, padx=20, pady=10)

        #ADD PRODUCT ID ENTRY TO THE GRID
        product_ID_entry=Entry(db_entry_frame,width=30)
        product_ID_entry.grid(row=0, column=1, padx=20, pady=10)

        #ADD NAME LABEL AND ENTRY BOX TO THE GRID
        db_name_label=Label(db_entry_frame,text="NAME",justify="right")
        db_name_label.grid(row=0,column=2, padx=20, pady=10)
        db_name_entry=Entry(db_entry_frame,width=30)
        db_name_entry.grid(row=0, column=3, padx=20, pady=10)

        #ADD QUANTITY LABEL AND ENTRY BOX TO THE GRID
        db_quan_label = Label(db_entry_frame, text="QUANTITY",justify="right")
        db_quan_label.grid(row=0, column=4, padx=20, pady=20)
        db_quan_entry = Entry(db_entry_frame, width=30)
        db_quan_entry.grid(row=0, column=5, padx=20, pady=20)

        #ADD PRICE LABEL AND ENTRY BOX TO THE GRID
        db_sellPrice_label = Label(db_entry_frame, text="SELLING PRICE",justify="right")
        db_sellPrice_label.grid(row=1, column=0, padx=20, pady=20)
        db_sellPrice_entry = Entry(db_entry_frame, width=30)
        db_sellPrice_entry.grid(row=1, column=1, padx=20, pady=20)

        #ADD COST LABEL AND ENTRY BOX TO THE GRID
        db_cost_label = Label(db_entry_frame, text="COST",justify="right")
        db_cost_label.grid(row=1, column=2, padx=20, pady=20)
        db_cost_entry = Entry(db_entry_frame, width=30)
        db_cost_entry.grid(row=1, column=3, padx=20, pady=20)

        #ADD CATEGORY LABEL AND ENTRY BOX TO THE GRID
        db_category_label = Label(db_entry_frame, text="CATEGORY",justify="right")
        db_category_label.grid(row=1, column=4, padx=20, pady=20)
        db_category_entry = Entry(db_entry_frame, width=30)
        db_category_entry.grid(row=1, column=5, padx=20, pady=20)

        for child in db_entry_frame.winfo_children():
            child.configure(font=('Times',18))

        #CLEAR RECORD ENTRIES FROM THE DATABASE
        def clear_record():
            product_ID_entry.delete(0,END)
            db_name_entry.delete(0,END)
            db_sellPrice_entry.delete(0,END)
            db_quan_entry.delete(0, END)
            db_cost_entry.delete(0, END)
            db_category_entry.delete(0, END)

        # SELECT ENTRIES FROM THE DATABASE
        # DELETE WHAT IS IN THE BOXES
        def select_record(x):
            product_ID_entry.delete(0,END)
            db_name_entry.delete(0,END)
            db_sellPrice_entry.delete(0,END)
            db_quan_entry.delete(0, END)
            db_cost_entry.delete(0, END)
            db_category_entry.delete(0, END)

            # REPOPULATE THE BOXES WITH THE SELECTED DATA FROM THE TABLE
            selected_record=db_view.focus()
            selected_values=db_view.item(selected_record,'values')

            # PUT THE SELECTED VALUES FROM THE DATABASE VIEW
            # INTO THE ENTRY BOXES FOR EDITING
            product_ID_entry.insert(0, selected_values[0])
            db_name_entry.insert(0, selected_values[1])
            db_sellPrice_entry.insert(0, selected_values[2])
            db_quan_entry.insert(0, selected_values[3])
            db_cost_entry.insert(0, selected_values[4])
            db_category_entry.insert(0, selected_values[5])

        # BIND THE SELECTION EVENT TO MOVE THE NEWLY SELECTED
        # RECORD/ROW INTO THE ENTRY BOXES
        db_view.bind("<ButtonRelease-1>", select_record)


        # CREATE A NEW FRAME TO ADD THE DATABASE BUTTONS
        # ASSIGN NAMES AND FUNCTION TO EACH BUTTON
        # REPLACE THE EXITING COMMAND FUNCTION WITH NEW FUNCTION
        db_button_frame = LabelFrame(canvas, text="Database Records Controls")
        db_button_frame.pack(fill="x", expand="yes", padx=10, pady=10)

        update_button=BakeryButton.BakeryButton(db_button_frame,
                                                height=button_height,
                                                width=button_width,
                                                text="UPDATE RECORD")
        update_button.grid(row=0,column=0,padx=10,pady=10, ipadx=10, ipady=10)

        add_records_button = BakeryButton.BakeryButton(db_button_frame,
                                                       height=button_height,
                                                       width=button_width,
                                                       text="NEW RECORD")
        add_records_button.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        remove_record_button = BakeryButton.BakeryButton(db_button_frame,
                                                         height=button_height,
                                                         width=button_width,
                                                         text="REMOVE RECORD")
        remove_record_button.grid(row=0, column=2, padx=10, pady=10, ipadx=10, ipady=10)

        remove_all_button = BakeryButton.BakeryButton(db_button_frame,
                                                      height=button_height,
                                                      width=button_width,
                                                      text="REMOVE ALL RECORDS")
        remove_all_button.grid(row=0, column=3, padx=10, pady=10, ipadx=10, ipady=10)

        move_up_button = BakeryButton.BakeryButton(db_button_frame,
                                                   height=button_height,
                                                   width=button_width,
                                                   text="MOVE RECORD UP")
        move_up_button.grid(row=0, column=4, padx=10, pady=10, ipadx=10, ipady=10)

        move_down_button=BakeryButton.BakeryButton(db_button_frame,
                                                   height=button_height,
                                                   width=button_width,
                                                   text="MOVE RECORD DOWN")
        move_down_button.grid(row=0,column=5,padx=10,pady=10, ipadx=10, ipady=10)

        select_button = BakeryButton.BakeryButton(db_button_frame,
                                                  height=button_height,
                                                  width=button_width,
                                                  text="CLEAR RECORD",command=clear_record)
        select_button.grid(row=0, column=6, padx=10, pady=10, ipadx=10, ipady=10)

        exit_button = BakeryButton.BakeryButton(db_button_frame,
                                                height=button_height,
                                                width=button_width,
                                                text="EXIT",command=lambda: DatabaseWindow.showBakeryWindow(self.root))
        exit_button.grid(row=1, column=3, padx=10, pady=10, ipadx=10, ipady=10)

        root.mainloop()
