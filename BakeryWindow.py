##########################################################################################################
## Application Bakery Point of Sale - 3FPS                                                              ##
## Bakery Window GUI: main window for point of sale. Products are listed to purchase                    ##
##                      transactions are maintained in the transaction view and totalized below         ##
##                      The window header provides File,Admin adn Help items for some navigation        ##
##                      Admin- login & logout + chart window selection                                  ##
##          Main window header has a few quick function buttons to sort by product category for quick   ##
##                      search                                                                          ##
## References: YouTube.com, Codemy.com, Stackoverflow.com, tutorialspoint.com, geeksforgeeks.org,       ##
##            pythonguides.com, anzeljg.github.io, & pythontutorial.net                                 ##
## Date: 06NOV21                                                                                        ##
##########################################################################################################
import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog,messagebox
from operator import itemgetter
import DataAccess, LoginWindow, About,Charts,BakeryButton


# CONSTANT VARIABLES USED THROUGHOUT THE CODE
# FRAME RELATIVE HEIGHT, RELATIVE WIDTH AND A COMMON COLOR
import Transaction

frame_rel_height = 0.9
frame_rel_width = 0.5
frame_color="#eae1df"
button_bg_color = "#f1b0a2"
category_bg_color=["#eba994","#e39888","#94a9eb","#94ebb8","#e7eb94"]
use_font='Times'


class Bakery:
    #DEFINE GLOBAL SETTING FOR ROOT WINDOW WIDTH AND HEIGHT
    global root_width
    root_width = 1900
    global root_height
    root_height = 1000
    global transaction_view_selected_item
    global transaction_item_id
    global gbl_transaction_in_progress
    global gbl_this_transaction
    gbl_transaction_in_progress = False
    gbl_this_transaction = Transaction.Transaction(1)       #setting up the transaction (empid)


    ##################################################################################################
    ## Creation of the initial Bakery window 'root'                                                 ##
    ## Some initial settings to put the window in the middle of the monitor display                 ##
    ## Add the menu item bar                                                                        ##
    ##################################################################################################
    def __init__(self, root):
        self.root = root
        self.root.title('Bakery')
        self.root.iconbitmap('CakesBakery.png')
        self.t=Transaction.Transaction(1)

        # GET THE DISPLAY WINDOW DIMENSIONS
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x = int(screen_width / 2 - root_width / 2)
        window_center_y = int(screen_height / 2 - root_height / 2)

        #SET THE ROOT WINDOW LOCATION ON THE DISPLAY
        self.root.geometry(f'{root_width}x{root_height}+{window_center_x}+{window_center_y}')

        #CREATE A MENU BAR
        app_menu=Menu(self.root)

        #FILE MENU ITEMS
        file_menu = Menu(app_menu, tearoff=0)
        file_menu.add_command(label="New",)
        file_menu.add_command(label="Open", )
        file_menu.add_command(label="Save", )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.destroy)
        app_menu.add_cascade(label="File",menu=file_menu)

        #ADMINISTRATOR MENU OPTIONS
        admin_menu = Menu(app_menu, tearoff=0)
        admin_menu.add_command(label="Login", command=lambda: showLoginWindow(self.root))
        admin_menu.add_command(label="Logout", command=doNothing())
        admin_menu.add_separator()
        admin_menu.add_command(label="Charts",command=lambda: showCharts(self.root))
        app_menu.add_cascade(label="Admin", menu=admin_menu)

        #HELP MENU OPTIONS
        help_menu=Menu(app_menu,tearoff=0)
        help_menu.add_command(label="Help",)
        help_menu.add_command(label="About",command=About.About)
        app_menu.add_cascade(label="Help",menu=help_menu)
        self.root.config(menu=app_menu)

        self.scrollable_Button_Frame=ttk.Frame()
        self.create_main_window()

    ##################################################################################################
    ## create_button_frame(self): Create a scrollable frame that the product selection buttons      ##
    ##                            will be placed for the user to select products                    ##
    ##                                                                                              ##
    ##################################################################################################
    def create_button_frame(self):
        Bakery.transaction_item_id=()
        bf = ttk.Style()
        bf.configure('new.TFrame', background='white', borderwidth=0, relief='flat')
        button_frame = ttk.Frame(self.root, style='new.TFrame')
        button_frame_label = LabelFrame(button_frame, text="PRODUCT SELECTION", font=(use_font, 24))
        button_frame.place(relwidth=frame_rel_width, relheight=frame_rel_height, relx=0.0, rely=0.1)

        #CREATE A CANVAS TO INSTALL OTHER WIDGETS OF THE APPLICATION INTO
        button_canvas = tk.Canvas(button_frame)
        button_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        #SCROLLBAR FOR THE BUTTON FRAME AND CONFIGURATION SETTINGS FOR THE BUTTON FRAME
        scrollbar = ttk.Scrollbar(button_frame, orient="vertical", command=button_canvas.yview)
        sbf = ttk.Style()
        sbf.configure('sbf.TFrame', background=frame_color, font=(use_font, 20), borderwidth=5,
                      relief='raised')
        scrollable_button_frame = ttk.Frame(button_canvas, style='sbf.TFrame')
        scrollable_button_frame.columnconfigure(0, weight=1)
        scrollable_button_frame.columnconfigure(1, weight=1)
        scrollable_button_frame.columnconfigure(2, weight=1)
        scrollable_button_frame.bind("<Configure>",
                                     lambda e: button_canvas.configure(scrollregion=button_canvas.bbox("all")))
        button_canvas.create_window((0, 0), window=scrollable_button_frame, anchor="nw")
        button_canvas.configure(yscrollcommand=scrollbar.set)
        # button_canvas.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right", fill="y")
        return scrollable_button_frame

    ##################################################################################################
    ## assign_product_buttons(self,var,data,Frame): Dynamically create filter buttons based on the  ##
    ##                            product categories that are in the product database 'category'    ##
    ##                            column. This is an added feature if there is time. Have been able ##
    ##                            to create the buttons dynamically elsewhere just need to finish   ##
    ##################################################################################################
    # ASSIGN THE TEXT AND COMMANDS TO THE PRODUCT BUTTONS TO ALLOW FOR SELECTION BY PRODUCT
    # OR REASSIGNMENT TO A SPECIFIC CATEGORY SELECTED FROM THE HEADER BUTTONS
    def assign_product_buttons(self,var,data,Frame):
        pass

    ##################################################################################################
    ## create_main_window(self): Create the main window and all other features. Buttons, transaction##
    ##                           item list, add and remove items, checkout, etc...                  ##
    ##                                                                                              ##
    ##################################################################################################
    #CREATE THE MAIN PORTION OF THE WINDOW,,,ADD THE BUTTONS FOR CHECKOUT SELECTION, ADD THE TOTAL WINDOW AND TOTAL LABEL
    def create_main_window(self):
        global root_width
        global root_height
        transaction_item_id=()

        ##################################################################################################
        ## selected_line_item(x): Determine what line item has focus in the transaction view "treeview" ##
        ##                        Get the transaction view selected item to be used in the function     ##
        ##                        selection                                                             ##
        ##################################################################################################
        def selected_line_item(x):
            selected_item = transaction_view.focus()  # The line item that has focus
            Bakery.transaction_view_selected_item = transaction_view.item(selected_item, 'values')
            Bakery.transaction_item_id = Bakery.transaction_view_selected_item
            return Bakery.transaction_item_id



        # GET THE PRODUCT INFORMATION FROM THE DATABASE:PRODUCT AND PUT INTO product_Data
        product_Data = DataAccess.listAllProduct()  # get the names and prices from the product table
        print("Prod_Data: ", product_Data )
        n = len(product_Data)  # get the length
        i = 0  # associate names and prices to the buttons
        j = 1

        # GET PRODUCT DATA CATEGORY NAMES FOR THE HEADER BUTTONS. LOOP THROUGH TO FIND THE HEADER CATEGORY AND NOTE ITS LOCATION
        # FOR THE ITEMGETTER() FUNCTION **NEED A SQL QUERY TO PULL THE COLUMNS OUT
        query = 'getProductCategory'
        if hasattr(DataAccess, query) and callable(func := getattr(DataAccess, query)):  # IF THE FUNCTION EXIST CALL IT
            *product_data_categories, = func()
        n = len(product_data_categories)  # THE CATEGORY TYPES HAVE THE COLUMN NAMES IN IT
        if n > 0:                           # If there are any, loop through and add them
            index = 0
            for quick_links in product_data_categories:
                db_product_categories = list(map(itemgetter(index), product_Data))
                product_category_names = list(set(db_product_categories))
                index += 1

        # MAIN WINDOW DIMENSIONS
        # ROOT STYLE SETTING FONT TO Times AND SIZE 20
        r=ttk.Style()
        r.theme_use('default')
        r.configure('.',background=button_bg_color,font=(use_font,20))
        canvas = tk.Canvas(master =self.root, width=root_width, height=root_height,bg = 'white')
        canvas.pack()

        # CREATE THE SCROLLABLE FRAME FOR THE PRODUCT SELECTION BUTTONS TO BE PLACED.
        scrollable_Button_Frame=self.create_button_frame()

        # ADD THE HEADER FRAME TO ADD BUTTONS FOR CATEGORY SELECTION
        appName_Frame = LabelFrame(self.root, text="", background=frame_color)
        appName_Frame['borderwidth']=1
        appName_Frame['relief']='raised'
        appName_Frame.place(relwidth=1.0, relheight=.1, relx=0, rely=0)
        appName = ttk.Label(appName_Frame, text="Bakery", font='Times 34 bold', background = frame_color)
        appName.pack(anchor=CENTER)

        # THESE BUTTONS ADDED TO THE HEADER WILL ALLOW FOR EITHER SELECTION BY PRODUCT TYPE OR ALPHABETICAL OR
        # SOME OTHER MEANS TO QUICKLY CHOOSE A CATEGORY, QUERY THE DATABASE TO GET THE PRODUCT CATEGORY TYPES AND PUSH THOSE
        # TO THE TOP HEADER FOR QUICK LINKS
        # for cat in product_category_names:
        #     ttk.Button(appName_Frame,text=cat,command=lambda cat=cat, data=product_Data: self.assign_product_buttons(cat,data,"scrollable_button_frame")).pack(side=LEFT,padx=10,expand=True)
        # ttk.Button(appName_Frame,text="Admin",command=lambda: showLoginWindow(self.root)).pack(side=LEFT, padx=10,expand=True)

        # transaction FRAME: ADD THE transaction FRAME TO THE RIGHT HALF OF THE SCREEN AND USE 90% OF THE SCREEN HEIGHT
        # (HEADER IS THE OTHER 10%)
        rf=ttk.Style()
        rf.configure('transaction.TFrame',background=frame_color, font=(use_font,20)) # #7AC5CD
        transaction_frame = ttk.Frame(self.root,style='transaction.TFrame')
        transaction_frame['borderwidth']=2
        transaction_frame['relief']='raised'
        transaction_frame.place(relwidth = frame_rel_width, relheight = frame_rel_height,relx=0.5,rely=0.1)

        #transaction FRAME STYLE WHERE ALL THE ITEMS FOR THIS TRANSACTION WILL BE DISPLAYED
        rfs = ttk.Style()
        # rfs.theme_use('default')
        rfs.configure("rs.Treeview",
                      background = frame_color,
                      foreground = "black",
                      rowheight = 25,
                      fieldbackground = frame_color,
                      font=(use_font, 20),
                      sticky='nsew') # #D3D3D3

        rfs.configure('rs.Treeview.Heading',
                      font=(use_font,22))
        rfs.map('TreeView',
                background =[('selected',"#ab90cb")])

        # ADD SCROLLBAR TO SCROLL THE TRANSACTION TREEVIEW
        transaction_scroll=Scrollbar(transaction_frame)
        transaction_scroll.pack(side=RIGHT,fill=Y)
        transaction_view=ttk.Treeview(transaction_frame,
                                 height=20,
                                 yscrollcommand=transaction_scroll.set,
                                 selectmode="extended",
                                 style='rs.Treeview')
        transaction_scroll.config(command=transaction_view.yview)



        # SET UP THE VIEW HEADINGS AND BIND THE SELECTION
        transaction_view['columns']=("NAME","ITEM ID","QUANTITY","PRICE")
        transaction_view.column("#0",width=0,stretch = NO)
        transaction_view.column("NAME", anchor=W,width=200)
        transaction_view.column("ITEM ID", anchor=W, width=200)
        transaction_view.column("QUANTITY", anchor=W, width=200)
        transaction_view.column("PRICE", anchor=W, width=200)
        transaction_view.heading("NAME", text="NAME", anchor=W)
        transaction_view.heading("ITEM ID", text="ITEM ID", anchor=W,)
        transaction_view.heading("QUANTITY",text="QUANTITY",anchor=W)
        transaction_view.heading("PRICE", text="PRICE", anchor=E)
        transaction_view.bind('<ButtonRelease-1>', selected_line_item)
        transaction_view.pack()
        transaction_frame_width = transaction_frame.winfo_screenwidth()

        #CREATE FRAME FOR THE TRANSACTION TOTAL
        tbf = ttk.Style()
        tbf.configure('tbf.TFrame',
                      background=frame_color,
                      font=(use_font, 20),
                      borderwidth=0,
                      relief='flat')
        total_frame = ttk.Frame(transaction_frame,
                                width=transaction_frame_width,
                                style='tbf.TFrame')
        total_frame.pack()

        #CREATE TRANSACTION LABEL AND TEXTBOX
        subtotal_textbox= Label(master=total_frame,
                                 text="Sub Total     $ {:.2f}".format(self.t.pre_tax),    #gbl_this_transaction.pre_tax
                                 foreground = 'black',
                                 background=frame_color,
                                 padx=10,
                                 pady=10,
                                 font=('Times',20),
                                 justify=tk.RIGHT)
        subtotal_textbox.pack(anchor='e')
        tax_textbox = Label(master=total_frame,
                            text="Tax     {:.0f} %".format(float(((self.t.tax-1)*100))),  #gbl_this_transaction.tax
                            foreground = 'black',
                            background=frame_color,
                            padx=10,
                            pady=10,
                            font=('Times', 20),
                            justify=tk.RIGHT)
        tax_textbox.pack(anchor='e')

        total_textbox = Label(master=total_frame,
                              text="Total     $ {:.2f}".format(self.t.final_cost),    #gbl_this_transaction.final_cost
                              foreground = 'black',
                              background=frame_color,
                              padx=10,
                              pady=10,
                              font=('Times', 20),
                              justify=tk.RIGHT)
        total_textbox.pack(anchor='e')


        # CREATE THE FRAME AND STYLE FOR THE TRANSACTION BUTTONS BELOW THE ITEM LIST
        # AND THE SUBTOTAL, TAX AND TOTAL
        transaction_button_frame=ttk.Frame(transaction_frame,width=transaction_frame_width,style='tbf.TFrame')
        transaction_button_frame.columnconfigure(0, weight=1)
        transaction_button_frame.columnconfigure(1, weight=1)
        transaction_button_frame.columnconfigure(2, weight=1)
        transaction_button_frame.pack(fill='both')
        tfb=ttk.Style()
        tfb_height = 60
        tfb_width = 200
        tfb.configure('tfb.TButton', font=(use_font, 20), background='grey', foreground='black',anchor=CENTER)
        remove_item_button=BakeryButton.BakeryButton(transaction_button_frame,
                                                     height = tfb_height,
                                                     width=tfb_width,
                                                     text="REMOVE ITEM",
                                                     style='tfb.TButton',
                                                     command= lambda: delete_selected())
        remove_item_button.grid(row=1,column=0,padx=20,pady=20)


        lookup_item_button = BakeryButton.BakeryButton(transaction_button_frame,
                                                       height=tfb_height,
                                                       width=tfb_width,
                                                       text="LOOKUP ITEM",
                                                       style='tfb.TButton')
        lookup_item_button.grid(row=1, column=1, padx=20, pady=20)

        discount_button = BakeryButton.BakeryButton(transaction_button_frame,
                                                    height = tfb_height,
                                                    width=tfb_width,
                                                    text="APPLY\nDISCOUNT",
                                                     style='tfb.TButton')
        discount_button.grid(row=1,column=2,padx=20,pady=20)
################
        checkout_button = BakeryButton.BakeryButton(transaction_button_frame,
                                                    height = tfb_height,
                                                    width=tfb_width,
                                                    text="CHECKOUT",
                                                     style='tfb.TButton',
                                                    command=lambda x=root_width,
                                                                   y=root_height,
                                                                   :checkOut_window(x,y,self.t)) #setup_Checkout(x,y,self.t)
        checkout_button.grid(row=1,column=3,padx=20,pady=20)

        # CREATE A BUTTON FOR PRODUCT SELECTION
        psb = ttk.Style()

        # COLOR CODE THE CATEGORY TYPES FOR THE PRODUCTS
        for productID, name, quan, price, cost, cat in product_Data:
            global category_bg_color
            # SAVE THIS FOR LATER. TAKE THE RETURNED CATEGORY VALUES FROM ABOVE AND EITHER ENUM OR
            # LOOP IN LOOP TO CHECK FOR THE CATEGORY AND SET A COLOR PROFILE TO THE BUTTON BASED
            # ON THE CATEGORY
            # if cat == "Bread":
            #     bg_color=category_bg_color[0]
            # elif cat=="Puff":
            #     bg_color=category_bg_color[1]
            # elif cat=="Filo":
            #     bg_color=category_bg_color[2]
            # elif cat=="Cake":
            #     bg_color=category_bg_color[3]
            # elif cat=="Cookie":
            #     bg_color=category_bg_color[4]

            # Add an item to the transaction
            psb.configure('b.TButton', font=(use_font, 20), foreground='black')
            selection_button = BakeryButton.BakeryButton(scrollable_Button_Frame, height=100, width=235, text=name,
                                                         style='b.TButton', command=lambda id=productID:addItem(self.t,id))
            Grid.rowconfigure(scrollable_Button_Frame, j, weight=1)
            Grid.columnconfigure(scrollable_Button_Frame, i, weight=1)
            selection_button.grid(row=j + 1,column=i, sticky="NESW", padx=20,pady=20)
            if i == 2:
                i = 0
                j += 1
            else:
                i += 1

            ##################################################################################
            ## addItem(id): pass in the id and create a new line item to show               ##
            ##              If the item exist already, increase quantity and price only     ##
            ##              Update the transaction line items                               ##
            ##################################################################################
            def addItem(t,id):
                global gbl_transaction_in_progress
                global gbl_this_transaction
                existing_item_ids = ()
                lookup_column = 2 - 1  # COLUMN NUMBER 2 HAS THE ITEMID ->SKU
                if not gbl_transaction_in_progress:
                    self.t=Transaction.Transaction(1)  #gbl_this_transaction=Transaction.Transaction(1) Create a new transaction, pass the employee id
                    gbl_transaction_in_progress = True
                for child in transaction_view.get_children():
                    existing_item_ids=transaction_view.item(child)["values"]
                if len(existing_item_ids)!=0:
                    line_item_index=0
                    match_found = False
                    for child in transaction_view.get_children():
                        *existing_item_ids,=transaction_view.item(child)["values"]
                        if id==existing_item_ids[1]:
                            # if an item is matched fill the data lineitem
                            # pass lineitem to increment_quantity
                            # insert updated lineitem in the original location
                            matched_lineitem=Transaction.LineItem(1,id,existing_item_ids[2])
                            transaction_view.delete(child)
                            nt=Transaction.LineItem.increment_quantity(matched_lineitem,id,1)
                            transaction_view.insert(parent='', index=line_item_index, text='',
                                                    values=(nt.nameID, nt.itemID, nt.quantity, "$ {:.2f}".format(nt.price)))
                            match_found = True  # If a match is found mark true and break the for loop
                            self.t.increment_item(id, 1)  #gbl_this_transaction.increment_item(id, 1)
                            break
                        line_item_index += 1    # Tracking which line number the loop is on

                    if match_found == False:    # Match wasn't found insert line item
                        self.t.increment_item(id,1)   #gbl_this_transaction.increment_item(id,1)
                        nt=Transaction.LineItem(1, id, 1)
                        transaction_view.insert(parent='', index='end', text='',
                                                values=(nt.nameID, nt.itemID, nt.quantity, "$ {:.2f}".format(nt.price)))

                else:   # It is the first entry insert the item
                    self.t.increment_item(id,1)   #gbl_this_transaction.increment_item(id,1)
                    nt=Transaction.LineItem(1, id, 1)
                    transaction_view.insert(parent='',
                                            index='end',
                                            text='',
                                            values=(nt.nameID,nt.itemID,nt.quantity,"{:.2f}".format(nt.price)))

                self.t.update_price()     # gbl_this_transaction.update_price()   Update the transaction prices
                subtotal_textbox.config(text="Sub Total     $ {:.2f}".format(self.t.pre_tax)) #gbl_this_transaction
                tax_textbox.config(text="Tax     {:.0f} %".format(float((self.t.tax-1)*100)))   #gbl_this_transaction
                total_textbox.config(text="Total     $ {:.2f}".format(self.t.final_cost))#gbl_this_transaction

            ##################################################################################################
            ## showPopUp_ItemNotSelected(msg): pass in a message to display to the user                     ##
            ##              This was initially made to let the user know they had not selected an item      ##
            ##              from the list to remove                                                         ##
            ##################################################################################################
            def showPopUp_ItemNotSelected(msg):
                tkinter.messagebox.showinfo(title="Info",
                                            message=msg)

            ##################################################################################################
            ## delete_selected(): delete the item selected by the user                                      ##
            ##              Called by 'remove_item_button'                                                  ##
            ##                                                                                              ##
            ##################################################################################################
            def delete_selected():  # Delete the item selected
                try:
                    x = transaction_view.selection()[0]  # Get the selected item
                    transaction_view.delete(x)  # Delete the selected item
                    i = int(Bakery.transaction_item_id[1])  # Covert the string to int
                    self.t.remove_item(i)  # gbl_this_transaction.remove_item(i) Delete the item from the transaction line item
                    self.t.update_price() #gbl_this_transaction.update_price()
                    subtotal_textbox.config(text="Sub Total     $ {:.2f}".format(self.t.pre_tax))#gbl_this_transaction
                    tax_textbox.config(text="Tax     {:.0f} %".format(float(((self.t.tax - 1) * 100))))#gbl_this_transaction
                    total_textbox.config(text="Total     $ {:.2f}".format(self.t.final_cost))#gbl_this_transaction
                except:
                    showPopUp_ItemNotSelected("An Item Was Not Selected.\nPlease Make A Selection And Try Again")

            # Start the checkout process
            def checkOut_window(x, y, t):

                def finalizeCashOut():
                    try:
                        cashAmount = float(enteredValue.get())
                        change = self.t.finalize_transaction(1, cashAmount)   #gbl_this_transaction.finalize_transaction(1, cashAmount)
                        checkout_change_value.config(text="$ {:.2f}".format(self.t.change_returned))
                    except:
                        showPopUp_ItemNotSelected("Cash Received is 0 or blank.\nPlease Enter A Value And Try Again")


                r_width = 850
                r_height = 350
                enteredValue = StringVar()
                checkout_popup_win = Toplevel(bg='gray',
                                              borderwidth=0)
                checkout_popup_win.title("Check Out: ")
                screen_width = x
                screen_height = y
                window_center_x = int(screen_width / 2 - r_width / 2)
                window_center_y = int(screen_height / 2 - r_height / 2)
                checkout_popup_win.geometry(f'{r_width}x{r_height}+{window_center_x}+{window_center_y}')
                checkout_canvas = Canvas(checkout_popup_win,
                                         bg='white',
                                         borderwidth=0)
                checkout_canvas.pack()
                checkout_frame1 = Frame(checkout_canvas,
                                        bg='white',
                                        borderwidth=0)
                checkout_frame1.grid(row=0,
                                     column=0,
                                     padx=10,
                                     pady=10)
                checkout_header_label = Label(checkout_frame1,
                                              borderwidth=2,
                                              text="Please Check The Cart To Make Sure All Items Are Accounted For",
                                              font=('Times', 24),
                                              background='white',
                                              pady=20)
                checkout_header_label.pack(anchor=CENTER)
                checkout_frame2 = Frame(checkout_canvas,
                                        borderwidth=0,
                                        bg='white')
                checkout_frame2.grid(row=1,
                                     column=0,
                                     pady=10,
                                     padx=10)
                checkout_total_label = Label(checkout_frame2,
                                             text='Total Balance: ',
                                             background='white',
                                             borderwidth=0,
                                             font=('Times', 24),
                                             pady=10)
                checkout_total_label.grid(row=0,
                                          column=0,
                                          sticky='e')
                checkout_total_amount = Label(checkout_frame2,
                                              borderwidth=0,
                                              font=('Times', 24),
                                              text="$ {:.2f}".format(t.final_cost),
                                              background='white')
                checkout_total_amount.grid(row=0,
                                           column=1,
                                           sticky='e')

                checkout_label = Label(checkout_frame2,
                                       text='Cash Entered: ',
                                       background='white',
                                       borderwidth=0,
                                       font=('Times', 24),
                                       pady=10)
                checkout_label.grid(row=1,
                                    column=0,
                                    sticky='e')
                checkout_amount_entered = Entry(checkout_frame2,
                                                textvariable=enteredValue,
                                                borderwidth=2,
                                                selectborderwidth=0,
                                                font=('Times', 24),
                                                justify=RIGHT)
                checkout_amount_entered.grid(row=1,
                                             column=1,
                                             sticky='e')

                checkout_change = Label(checkout_frame2,
                                        text="Change to give:",
                                        borderwidth=0,
                                        background='white',
                                        font=('Times', 24))
                checkout_change.grid(row=2,
                                     column=0,
                                     sticky='e')

                checkout_change_value = Label(checkout_frame2,
                                              text=self.t.change_returned,
                                              background='white',
                                              borderwidth=0,
                                              font=('Times', 24))
                checkout_change_value.grid(row=2,
                                           column=1,
                                           sticky='e')

                checkout_frame3 = Frame(checkout_canvas,
                                        bg='white')
                checkout_frame3.grid(row=2,
                                     column=0,
                                     pady=10,
                                     padx=10)
                checkout_finalize = Button(checkout_frame3,             #Checkout button
                                           text="Complete",
                                           font=('Times', 24),
                                           height=2,
                                           width=20,
                                           command=lambda: finalizeCashOut())
                checkout_finalize.grid(row=0,column=0,padx=10,pady=10)

                checkout_clear_list = Button(checkout_frame3,             #Finalize clear item list
                                             text="Finish Transaction",
                                             font=('Times', 24),
                                             height=2,
                                             width=20,
                                             command=lambda: doNothing())
                checkout_clear_list.grid(row=0,column=1,padx=10,pady=10)


# Show the charts window
def showCharts(e):
    e.destroy()
    newRoot=Tk()
    application=Charts.Graph(newRoot)
    newRoot.mainloop()


# Show the login window to get to the database view
def showLoginWindow(e):
    e.destroy()
    newRoot=Tk()
    application=LoginWindow.Login(newRoot)
    newRoot.mainloop()


# Do nothing
def doNothing():
    pass


def setup_Checkout(x,y):
    x=x
    y=y
    purchase_total=gbl_this_transaction
    checkOut_window(x,y,purchase_total)



def bakery_frame(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0,weight = 1)
    frame.columnconfigure(1,weight = 3)
    frame['borderwidth'] =5
    frame['relief'] = 'raised'
    return frame


    root.mainloop()


###############
# Notes:    1.  Left off working on the checkout window. The transaction is not being passed to calculated the change, etc...
#           2.  Also noticed that the price in the transaction view will increment 2x so a $0.50 item will end up showing
#               the price at $1.00