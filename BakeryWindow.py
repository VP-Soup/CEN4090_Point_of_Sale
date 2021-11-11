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

from tkinter import *
import tkinter as tk
from tkinter import ttk
from operator import itemgetter
import DataAccess, LoginWindow, About,Charts,BakeryButton


# CONSTANT VARIABLES USED THROUGHOUT THE CODE
# FRAME RELATIVE HEIGHT, RELATIVE WIDTH AND A COMMON COLOR
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

    def __init__(self, root):
        self.root = root
        self.root.title('Bakery')
        self.root.iconbitmap('CakesBakery.png')

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

    # BUTTON FRAME: CREATE A SCROLLABLE WINDOW TO SCROLL THE PRODUCT BUTTONS.
    def create_button_frame(self):
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


    # ASSIGN THE TEXT AND COMMANDS TO THE PRODUCT BUTTONS TO ALLOW FOR SELECTION BY PRODUCT
    # OR REASSIGNMENT TO A SPECIFIC CATEGORY SELECTED FROM THE HEADER BUTTONS
    def assign_product_buttons(self,var,data,Frame):
        pass


    #CREATE THE MAIN PORTION OF THE WINDOW,,,ADD THE BUTTONS FOR CHECKOUT SELECTION, ADD THE TOTAL WINDOW AND TOTAL LABEL
    def create_main_window(self):

        # GET THE PRODUCT INFORMATION FROM THE DATABASE:PRODUCT AND PUT INTO product_Data
        product_Data = DataAccess.listAllProducts()  # get the names and prices from the product table
        print("Prod_Data: ", product_Data )
        n = len(product_Data)  # get the length
        i = 0  # associate names and prices to the buttons
        j = 1

        # GET PRODUCT DATA CATEGORY NAMES FOR THE HEADER BUTTONS. LOOP THROUGH TO FIND THE HEADER CATEGORY AND NOTE ITS LOCATION
        # FOR THE ITEMGETTER() FUNCTION **NEED A SQL QUERY TO PULL THE COLUMNS OUT
        index=5
        # for table_columns in product_Data:
        #     if table_columns=="Category":
        #         item=index
        #     else:
        #         index+=1
        db_product_categories=list(map(itemgetter(index),product_Data))
        product_category_names=list(set(db_product_categories))
        #product_category_names.append("admin")


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
        appName_Frame['borderwidth']=5
        appName_Frame['relief']='raised'
        appName_Frame.place(relwidth=1.0, relheight=.1, relx=0, rely=0)
        appName = ttk.Label(appName_Frame, text="Bakery", font='Times 24 bold', background = frame_color)
        appName.pack()

        # THESE BUTTONS ADDED TO THE HEADER WILL ALLOW FOR EITHER SELECTION BY PRODUCT TYPE OR ALPHABETICAL OR
        # SOME OTHER MEANS TO QUICKLY CHOOSE A CATEGORY, QUERY THE DATABASE TO GET THE PRODUCT CATEGORY TYPES AND PUSH THOSE
        # TO THE TOP HEADER FOR QUICK LINKS
        for cat in product_category_names:
            ttk.Button(appName_Frame,text=cat,command=lambda cat=cat, data=product_Data: self.assign_product_buttons(cat,data,"scrollable_button_frame")).pack(side=LEFT,padx=10,expand=True)
        ttk.Button(appName_Frame,text="Admin",command=lambda: showLoginWindow(self.root)).pack(side=LEFT, padx=10,expand=True)

        # transaction FRAME: ADD THE transaction FRAME TO THE RIGHT HALF OF THE SCREEN AND USE 90% OF THE SCREEN HEIGHT
        # (HEADER IS THE OTHER 10%)
        rf=ttk.Style()
        rf.configure('transaction.TFrame',background=frame_color, font=(use_font,20)) # #7AC5CD
        transaction_frame = ttk.Frame(self.root,style='transaction.TFrame')
        transaction_frame['borderwidth']=5
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
        transaction_view['columns']=("ITEM","QUANTITY","PRICE")
        transaction_view.column("#0",width=0,stretch = NO)
        transaction_view.column("ITEM", anchor=W,width=250)
        transaction_view.column("QUANTITY", anchor=E, width=250)
        transaction_view.column("PRICE", anchor=E,width=250)
        transaction_view.heading("ITEM", text="ITEM", anchor=W)
        transaction_view.heading("QUANTITY",text="QUANTITY",anchor=CENTER)
        transaction_view.heading("PRICE", text="PRICE", anchor=E)
        transaction_view.pack()

        transaction_frame_width = transaction_frame.winfo_screenwidth()
        print("transaction view width: ", transaction_frame_width)

        #CREATE FRAME FOR THE TRANSACTION TOTAL
        tbf = ttk.Style()
        tbf.configure('tbf.TFrame',
                      background=frame_color,
                      font=(use_font, 20),
                      borderwidth=0,
                      relief='flat')
        total_frame = ttk.Frame(transaction_frame,width=transaction_frame_width,style='tbf.TFrame')
        total_frame.pack()
        #CREATE TRANSACTION LABEL AND TEXTBOX
        subtotal_textbox = ttk.Label(master=total_frame,
                                  text="Sub Total     $ 0.00",
                                  foreground = 'black',
                                  background=frame_color,
                                  padding=10,
                                  justify=tk.RIGHT)
        subtotal_textbox.pack(anchor='e')
        tax_textbox = ttk.Label(master=total_frame,
                                  text="Tax     $ 0.00",
                                  foreground = 'black',
                                  background=frame_color,
                                  padding=10,
                                  justify=tk.RIGHT)
        tax_textbox.pack(anchor='e')

        total_textbox = ttk.Label(master=total_frame,
                                  text="Total     $ 0.00",
                                  foreground = 'black',
                                  background=frame_color,
                                  padding=10,
                                  justify=tk.RIGHT)
        total_textbox.pack(anchor='e')


        transaction_button_frame=ttk.Frame(transaction_frame,width=transaction_frame_width,style='tbf.TFrame')
        transaction_button_frame.columnconfigure(0, weight=1)
        transaction_button_frame.columnconfigure(1, weight=1)
        transaction_button_frame.columnconfigure(2, weight=1)
        transaction_button_frame.pack(fill='both')
        tfb=ttk.Style()
        tfb_height = 60
        tfb_width = 200
        tfb.configure('tfb.TButton', font=(use_font, 20), background='grey', foreground='black')
        remove_item_button=BakeryButton.BakeryButton(transaction_button_frame,
                                                     height = tfb_height,
                                                     width=tfb_width,
                                                     text="REMOVE ITEM",
                                                     style='tfb.TButton')
        remove_item_button.grid(row=1,column=0,padx=20,pady=20)

        discount_button = BakeryButton.BakeryButton(transaction_button_frame,
                                                    height = tfb_height,
                                                    width=tfb_width,
                                                    text="APPLY DISCOUNT",
                                                     style='tfb.TButton')
        discount_button.grid(row=1,column=1,padx=20,pady=20)

        checkout_button = BakeryButton.BakeryButton(transaction_button_frame,
                                                    height = tfb_height,
                                                    width=tfb_width,
                                                    text="CHECKOUT",
                                                     style='tfb.TButton')
        checkout_button.grid(row=1,column=2,padx=20,pady=20)

        # CREATE A BUTTON FOR PRODUCT SELECTION
        psb = ttk.Style()

        # COLOR CODE THE CATEGORY TYPES FOR THE PRODUCTS
        for productID, name, quan, price, cost, cat in product_Data:
            x=''
            global category_bg_color
            if cat == "Bread":
                bg_color=category_bg_color[0]
            elif cat=="Puff":
                bg_color=category_bg_color[1]
            elif cat=="Filo":
                bg_color=category_bg_color[2]
            elif cat=="Cake":
                bg_color=category_bg_color[3]
            elif cat=="Cookie":
                bg_color=category_bg_color[4]
            psb.configure('b.TButton', font=(use_font, 20), background=bg_color, foreground='black')
            selection_button=BakeryButton.BakeryButton(scrollable_Button_Frame,height = 100,width=235,text=name,
                                      style='b.TButton',command=lambda name=name,price=price: transaction_view.insert
                                      (parent='', index='end', text='', values=(name,x,price)))
            Grid.rowconfigure(scrollable_Button_Frame, j, weight=1)
            Grid.columnconfigure(scrollable_Button_Frame, i, weight=1)
            selection_button.grid(row=j + 1,column=i, sticky="NESW", padx=20,pady=20)
            if i == 2:
                i = 0
                j += 1
            else:
                i += 1

def showCharts(e):
    e.destroy()
    newRoot=Tk()
    application=Charts.Graph(newRoot)
    newRoot.mainloop()

def showLoginWindow(e):
    e.destroy()
    newRoot=Tk()
    application=LoginWindow.Login(newRoot)
    newRoot.mainloop()

def doNothing():
    pass


def bakery_frame(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0,weight = 1)
    frame.columnconfigure(1,weight = 3)
    frame['borderwidth'] =5
    frame['relief'] = 'raised'
    return frame


    root.mainloop()


