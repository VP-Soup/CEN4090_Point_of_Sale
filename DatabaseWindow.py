##########################################################################################################
## Application Bakery Point of Sale - 3FPS                                                              ##
## Bakery Database GUI: interface with the products datatable for product addition, removal, etc        ##
##                      Main area is the treeview for the database records, followed by an area to      ##
##                      record new product information. The last section is for the sql commands to     ##
##                      edit the records in the database.                                               ##
## References: YouTube.com, Codemy.com, Stackoverflow.com, tutorialspoint.com, geeksforgeeks.org,       ##
##            pythonguides.com, anzeljg.github.io, & pythontutorial.net                                 ##
## Date: 28NOV21                                                                                        ##
##########################################################################################################
import tkinter

from tkinter import *
import tkinter as tk
from tkinter import ttk
import BakeryButton, DataAccess,BakeryWindow,Charts,About


class DatabaseWindow:
    #GLOBAL COUNT VARIABLE FOR THE ROWS ODD/EVEN
    global count
    count=0
    global db_being_viewed
    db_being_viewed=""

    def doNothing():
        pass

    def showBakeryWindow(e,eid):
        e.destroy()
        newRoot = Tk()
        application = BakeryWindow.Bakery(newRoot,eid)
        newRoot.mainloop()

    # Show the charts window
    def showCharts(e, eid):
        e.destroy()
        newRoot = Tk()
        application = Charts.Graph(newRoot, eid)
        newRoot.mainloop()

    def __init__(self, root, eid):
        #SET THE WINDOW DIMENSIONS
        button_width=175
        button_height=70
        self.root = root
        self.root.title('Database Entry')
        self.eid = eid
        entries = []    #The values in the entry boxes
        global db_being_viewed
        db_being_viewed = "Product"
        #GET THE DISPLAY WINDOW DIMENSIONS
        screen_width=root.winfo_screenwidth()
        screen_height=root.winfo_screenheight()

        #FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x=int(screen_width/2-screen_width/2)
        window_center_y=int(screen_height/2-screen_height/2)

        #SET THE ROOT WINDOW LOCATION ON THE DISPLAY
        root.geometry(f'{screen_width}x{screen_height}+{window_center_x}+{window_center_y}')

        #SET THE STYLE OF THE DATABASE ENTRY
        db_style=ttk.Style()
        db_style.configure('db.Treeview',
                           background="#eae1df",
                           foreground='black',
                           rowheight=40,
                           fieldbackground="#eae1df",
                           ipady=20,
                           font=('Times',20))
        db_style.configure('db.Treeview.Heading',
                           rowheight=40,
                           font=('Times',20,'bold'))

        db_style.map('db.Treeview',
                     background=[('selected','#347083')])
        db_frame=ttk.Frame(root,height = screen_height/2, width=screen_width)
        db_frame['padding']=5
        db_frame['borderwidth']=0
        db_frame['relief']='flat'
        db_frame.grid_rowconfigure(0,weight = 1)
        db_frame.grid_columnconfigure(0, weight = 1)
        db_frame.pack(expand = True)

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

        db_view['columns']=("ID","Name","Quantity","Selling Price","Cost","Category")

        db_view.column("#0",
                       width=0,
                       stretch=NO)
        db_view.column("ID",
                       anchor=W,
                       stretch=YES)
        db_view.column("Name",
                       anchor=W,
                       stretch=YES)
        db_view.column("Quantity",
                       anchor=W,
                       stretch=YES)
        db_view.column("Selling Price",
                       anchor=W,
                       stretch=YES)
        db_view.column("Cost",
                       anchor=W,
                       stretch=YES)
        db_view.column("Category",
                       anchor=W,
                       stretch=YES)


        #DATABASE VIEW COLUMN HEADINGS
        db_view.heading("#0",text="")
        db_view.heading("ID", text="ID", anchor=W)
        db_view.heading("Name", text="Name", anchor=W)
        db_view.heading("Quantity", text="Quantity", anchor=W)
        db_view.heading("Selling Price", text="Selling Price", anchor=W)
        db_view.heading("Cost", text="Cost", anchor=W)
        db_view.heading("Category", text="Category", anchor=W)

        #SET ALTERNATING COLORS FOR THE DATABASE ENTRIES
        db_view.tag_configure('oddentry',background='#eae1df')
        db_view.tag_configure('evenentry',background='#f1b0a2')

        #SQL QUERY TO RETURN ALL THE PRODUCTS FROM THE DATABASE ADD ASSIGN COLORS TO THE ROWS
        db_entry=DataAccess.listAllProduct()
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
        db_entry_frame=LabelFrame(root,text="Database Entry")
        db_entry_frame.pack(fill="x",expand=Y,padx=20,pady=20)

        #ADD PRODUCT ID LABEL TO THE GRID
        product_ID_label = Label(db_entry_frame,text="Product ID",justify="right")
        product_ID_label.grid(row=0, column=0, padx=20, pady=10)

        #ADD PRODUCT ID ENTRY TO THE GRID
        product_ID_entry=Entry(db_entry_frame,width=30)
        entries.append(product_ID_entry)
        product_ID_entry.grid(row=0, column=1, padx=20, pady=10)

        #ADD NAME LABEL AND ENTRY BOX TO THE GRID
        db_name_label=Label(db_entry_frame,text="Name",justify="right")
        db_name_label.grid(row=0,column=2, padx=20, pady=10)
        db_name_entry=Entry(db_entry_frame,width=30)
        entries.append(db_name_entry)
        db_name_entry.grid(row=0, column=3, padx=20, pady=10)

        #ADD QUANTITY LABEL AND ENTRY BOX TO THE GRID
        db_quan_label = Label(db_entry_frame, text="Quantity",justify="right")
        db_quan_label.grid(row=0, column=4, padx=20, pady=20)
        db_quan_entry = Entry(db_entry_frame, width=30)
        entries.append(db_quan_entry)
        db_quan_entry.grid(row=0, column=5, padx=20, pady=20)

        #ADD PRICE LABEL AND ENTRY BOX TO THE GRID
        db_sellPrice_label = Label(db_entry_frame, text="Selling Price $",justify="right")
        db_sellPrice_label.grid(row=1, column=0, padx=20, pady=20)
        db_sellPrice_entry = Entry(db_entry_frame, width=30)
        entries.append(db_sellPrice_entry)
        db_sellPrice_entry.grid(row=1, column=1, padx=20, pady=20)

        #ADD COST LABEL AND ENTRY BOX TO THE GRID
        db_cost_label = Label(db_entry_frame, text="Cost $",justify="right")
        db_cost_label.grid(row=1, column=2, padx=20, pady=20)
        db_cost_entry = Entry(db_entry_frame, width=30)
        entries.append(db_cost_entry)
        db_cost_entry.grid(row=1, column=3, padx=20, pady=20)

        #ADD CATEGORY LABEL AND ENTRY BOX TO THE GRID
        db_category_label = Label(db_entry_frame, text="Category",justify="right")
        db_category_label.grid(row=1, column=4, padx=20, pady=20)
        db_category_entry = Entry(db_entry_frame, width=30)
        entries.append(db_category_entry)
        db_category_entry.grid(row=1, column=5, padx=20, pady=20)

        for child in db_entry_frame.winfo_children():
            child.configure(font=('Times',20))

        #CLEAR RECORD ENTRIES FROM THE DATABASE
        def clear_record():
            product_ID_entry.delete(0,END)
            db_name_entry.delete(0,END)
            db_sellPrice_entry.delete(0,END)
            db_quan_entry.delete(0, END)
            db_cost_entry.delete(0, END)
            db_category_entry.delete(0, END)

        #SELECT ENTRIES FROM THE DATABASE
        # DELETE WHAT IS IN THE BOXES
        def select_record(x):
            for widget in db_entry_frame.winfo_children():
                if isinstance(widget,tkinter.Entry):
                    widget.delete(0,END)

            # RE-POPULATE THE BOXES WITH THE SELECTED DATA FROM THE TABLE
            selected_record=db_view.focus()
            selected_values=db_view.item(selected_record,'values')

            # Enter the selected record into the textboxes
            v = len(selected_values)
            index=0
            for widget in db_entry_frame.winfo_children():
                if isinstance(widget,tkinter.Entry):
                    widget.insert(0,selected_values[index])
                    index+=1

        db_view.bind("<ButtonRelease-1>", select_record)    # Bind a button event to a record selection

        def set_button_commands():
            update_button = BakeryButton.BakeryButton(dbbutton_frame,
                                                      height=button_height,
                                                      width=button_width,
                                                      text="UPDATE RECORD",
                                                      command=lambda query='update',t=db_being_viewed: db_button_pressed_event(query,t,entries))
            update_button.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)

            add_records_button = BakeryButton.BakeryButton(dbbutton_frame,
                                                           height=button_height,
                                                           width=button_width,
                                                           text="INSERT NEW RECORD",
                                                           command=lambda query='insert', t=db_being_viewed: db_button_pressed_event(query, t, entries))
            add_records_button.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)

            remove_record_button = BakeryButton.BakeryButton(dbbutton_frame,
                                                             height=button_height,
                                                             width=button_width,
                                                             text="DELETE RECORD",
                                                             command=lambda query='delete',t=db_being_viewed: db_button_pressed_event(query, t, entries))
            remove_record_button.grid(row=0, column=2, padx=10, pady=10, ipadx=10, ipady=10)

            select_button = BakeryButton.BakeryButton(dbbutton_frame,
                                                      height=button_height,
                                                      width=button_width,
                                                      text="CLEAR ENTRY", command=clear_record)
            select_button.grid(row=0, column=3, padx=10, pady=10, ipadx=10, ipady=10)

            exit_button = BakeryButton.BakeryButton(dbbutton_frame,
                                                    height=button_height,
                                                    width=button_width,
                                                    text="EXIT", command=lambda: DatabaseWindow.showBakeryWindow(root,self.eid))
            exit_button.grid(row=0, column=4, padx=10, pady=10, ipadx=10, ipady=10)

        def db_button_pressed_event(q,t,e):     # When a db event button is pressed it will pass the query and the
            return_string=""                    # entries list
            query_string= q+t
            number_of_variables=len(e)

            if hasattr(DataAccess, query_string) and callable(func := getattr(DataAccess, query_string)):  # If the fx exist call it
                if q == 'delete':
                    return_string = func(e[0].get())
                elif number_of_variables==4:
                    return_string = func(e[0].get(),e[1].get(),e[2].get(),e[3].get())
                elif number_of_variables==5:
                    return_string = func(e[0].get(), e[1].get(), e[2].get(), e[3].get(),e[4].get())
                elif number_of_variables==6:
                    return_string = func(e[0].get(), e[1].get(), e[2].get(), e[3].get(),e[4].get(),e[5].get())
                setup_query=getMenuItemCommand(t)
                setUp(setup_query,t)
            set_button_commands()

        #CREATE A NEW FRAME TO ADD THE RECORD ENTRY AND DELETE BUTTONS
        dbbutton_frame = LabelFrame(root, text="Database Records Controls")
        for i in range (5): # For loop to enable equal column widths for the buttons
            dbbutton_frame.grid_columnconfigure(i,weight=1)
        dbbutton_frame.pack(fill="x", expand="yes", padx=20, pady=20)
        set_button_commands()

        # CREATE A MENU BAR
        app_menu = Menu(root)

        # FILE MENU ITEMS
        file_menu = Menu(app_menu, tearoff=0)
        # file_menu.add_command(label="New", )
        # file_menu.add_command(label="Open", )
        # file_menu.add_command(label="Save", )
        # file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.destroy)
        app_menu.add_cascade(label="File", menu=file_menu)

        # ADMINISTRATOR MENU OPTIONS
        admin_menu = Menu(app_menu, tearoff=0)
        admin_menu.add_command(label="Login", command=lambda: BakeryWindow.showLoginWindow(root))
        admin_menu.add_command(label="Logout", command=lambda: BakeryWindow.Bakery(root,self.eid))
        admin_menu.add_separator()
        admin_menu.add_command(label="Charts", command=lambda: DatabaseWindow.showCharts(self.root, self.eid))
        app_menu.add_cascade(label="Admin", menu=admin_menu)


        # DATABASE MENU OPTIONS GET TABLE NAMES AND ADD TO THE MENU
        dbase_menu = Menu(app_menu, tearoff=0)
        table_names = DataAccess.listTables()
        for table in table_names:
            # QUERY STRING TO A COMMAND FOR LISTALL"TABLE"()
            # PASS TO THE SETUP FUNCTION THE VIEW TO USE, THE TRANSACTION CLASS FUNCTION TO USE
            # AND THE TABLE THAT IS BEING USED
            # sql_query_command = f"{table}"
            # print("table: query:", table, sql_query_command)
            dbase_menu.add_command(label=table,
                                   command=lambda view=db_view, boundm=table: setUp(getMenuItemCommand(boundm), boundm))
        app_menu.add_cascade(label="Database", menu=dbase_menu) # ADD MENU ITEMS TO THE WINDOW TITLE BAR


        def getMenuItemCommand(tag):
            global db_being_viewed      # Keep track of the database being viewed
            command=f"view{tag}Table"   # Table to view
            db_being_viewed = tag       # Update the database being viewed for the buttons variable 't'
            set_button_commands()       # Update the button command
            return command
        # HELP MENU OPTIONS
        help_menu = Menu(app_menu, tearoff=0)
        help_menu.add_command(label="Help", )
        help_menu.add_command(label="About", command=About.About)
        app_menu.add_cascade(label="Help", menu=help_menu)
        root.config(menu=app_menu)

        #Button click event to refresh the screen


        # SETUP FUNCTION TO POPULATE THE DATABASE VIEW WITH DIFFERENT MENU SELECTIONS
        def setUp(query,table):

            dbcolumns_names = []  # TABLE NAMES RETRIEVED FROM A TABLE
            count = 0  # ODD AND EVEN ROWS WILL BE DIFFERENT BG COLORS ALSO USED FOR IID
            entries.clear()

            for i in db_view.get_children(): # CLEAR THE TREEVIEW OF EXISTING ENTRIES
                db_view.delete(i)

            # CHECK IF THE QUERY EXIST IN THE DataAccess LAYER AND THEN REQUEST
            # THE *'VARIABLE', REPRESENTS A TUPLE TO RECEIVE DATA - GOOD TO REMEMBER
            # DATA RETURNED FROM THE QUERY TO PULL APART HAVE TO HAVE cur
            cur=()
            if hasattr(DataAccess,query) and callable(func := getattr(DataAccess,query)): #IF THE FUNCTION EXIST CALL IT
                *cur,=func()
            n = len(cur[0].description)     # THE CURSER.DESCRIPTION HAS THE COLUMN NAMES IN IT
            if n>0:
                db_entry_frame.winfo_children()                 # Get widgets in the db entry frame
                for widget in db_entry_frame.winfo_children():  # Delete the widgets in the frame to create new widgets
                    widget.destroy()                            # connected to the database that will be viewed
                l=Label()
                e=Entry()                                       # Keep track of the entry boxes to pass to the...
                label_index=0                                   # ...def db_button_pressed_event(q,t,e)
                entry_index=0
                column_number=0
                row_number=0
                for index in range(0, n):           # GET THE TABLE NAMES OUT FOR THE HEADERS
                    dbcolumns_names.append(cur[0].description[index][0])
                    if query == 'viewEmployeeTable' and index == 0:
                        pass
                    else:
                        l[label_index] = Label(db_entry_frame,text=cur[0].description[index][0],
                                                justify="right").grid(row=row_number,
                                                column=column_number,
                                                padx=20, pady=20)
                        label_index+=1
                        column_number+=1
                        e = Entry(db_entry_frame,width=30)  #Create new entry boxes for the number of
                        e.grid(row=row_number,              #Colums in the new table
                               column=column_number,
                               padx=20,
                               pady=20)
                        entries.append(e)                   #Add the entry text to a list for use in button
                        entry_index+=1
                        column_number+=1
                        if column_number==6:                # Add label and entry box 3 pairs
                            column_number=0                 # start over at column 0
                            row_number+=1                   # Increment row
                for child in db_entry_frame.winfo_children():
                    child.configure(font=('Times', 20))
            db_view['columns'] = dbcolumns_names  # Define the column names and headers

            for c in dbcolumns_names:          # LOOP THROUGH THE NAMES AND ADD THE HEADERS TO THE VIEW
                db_view.column(c, anchor=W, stretch=YES)

            # DATABASE VIEW COLUMN HEADINGS
            for c in dbcolumns_names:          # SET THE HEADINGS
                db_view.heading(c, text=c, anchor=W)

                # SET ALTERNATING COLORS FOR THE DATABASE ENTRIES
                db_view.tag_configure('oddentry', background='#eae1df')
                db_view.tag_configure('evenentry', background='#f1b0a2')

            # MAKE UP THE QUERY NAME TO CALL
            # CHECK IF THE QUERY EXIST IN THE DataAccess LAYER AND THEN REQUEST
            # THE DATA AND PUT IT IN dbENTRY
            dbentry=()
            list_all_query=f"listAll{table}"
            if hasattr(DataAccess, list_all_query) and callable(func := getattr(DataAccess, list_all_query)):
                dbentry = func()                # DATA FROM THE TABLE

            entry_length=len(dbentry)           # LENGTH OF DATA TUPLES TO LOOP THROUGH
            for index in range(entry_length):   # LOOP THROUGH THE DATA AND ENTER IT INTO THE DATABASE VIEW
                if (table == 'Employee'):
                    value = list(dbentry[index])
                    value[4] = '*****'
                    value = tuple(value)
                else:
                    value = dbentry[index]
                if count % 2 == 0:                # SET THIS ROW WITH A BACKGROUND COLOR DIFFERENT THAN THE NEXT
                    db_view.insert("", 'end', iid=count, text='', values=value, tags=('evenentry',))
                elif count % 2 == 1:
                    db_view.insert("",'end', iid=count, text='', values=value, tags=('oddentry',))
                count += 1
                index += 1

            db_view.bind("<ButtonRelease-1>", select_record)  # Bind a button event to a record selection

        root.mainloop()
