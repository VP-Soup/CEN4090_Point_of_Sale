from tkinter import *
import tkinter as tk
from tkinter import ttk
from operator import itemgetter
import DataAccess, LoginWindow, ViewDatabase,Transaction,DatabaseWindow,BakeryButton

# Bakery GUI window
# CONSTANT VARIABLES USED THROUGHOUT THE CODE
# FRAME RELATIVE HEIGHT, RELATIVE WIDTH AND A COMMON COLOR
frame_rel_height = 0.9
frame_rel_width = 0.5
frame_color="#eae1df"
button_bg_color = "#f1b0a2"
category_bg_color=["#eba994","#e39888","#94a9eb","#94ebb8","#e7eb94"]
use_font='Times'

class Bakery:

    def __init__(self, root):
        self.root = root
        self.root.title('Bakery')
        self.root.iconbitmap('CakesBakery.png')

        app_menu=Menu(self.root)

        # FILE MENU ITEMS
        # file_menu = Menu(app_menu, tearoff=0)
        # file_menu.add_command(label="New",)
        # file_menu.add_separator()
        # file_menu.add_command(label="Exit", command=self.root.quit)
        # app_menu.add_cascade(label="File",menu=file_menu)
        #
        # admin_menu = Menu(app_menu, tearoff=0)
        # admin_menu.add_command(label="Login", command=showLoginWindow(x))
        # admin_menu.add_separator()
        # admin_menu.add_command(label="Logout", command=showLoginWindow())
        # app_menu.add_cascade(label="Admin", menu=admin_menu)

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

        button_canvas = tk.Canvas(button_frame)
        button_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar = ttk.Scrollbar(button_frame, orient="vertical", command=button_canvas.yview)

        sbf = ttk.Style()
        sbf.configure('sbf.TFrame', background=frame_color, font=(use_font, 20), borderwidth=5,
                      relief='raised')  # #7AC5CD
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
        #self.root.geometry = ('1920x1080')
        r=ttk.Style()
        r.theme_use('default')
        r.configure('.',background=button_bg_color,font=(use_font,20))
        canvas = tk.Canvas(master =self.root, width=1920, height=1080,bg = 'white')
        canvas.pack()


        # CREATE THE SCROLLABLE FRAME FOR THE PRODUCT SELECTION BUTTONS TO BE PLACED.
        scrollable_Button_Frame=self.create_button_frame()

        # ADD THE HEADER
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
        rfs.theme_use('default')
        rfs.configure("TreeView", background = frame_color, foreground = "black", rowheight = 200,
                        fieldbackground = frame_color, font=(use_font, 30),sticky='nsew') # #D3D3D3
        rfs.map('TreeView', background =[('selected',"#ab90cb")])

        # ADD SCROLLBAR TO SCROLL THE transaction
        transaction_scroll=Scrollbar(transaction_frame)
        transaction_scroll.pack(side=RIGHT,fill=Y)
        transaction_view=ttk.Treeview(transaction_frame,
                                 height=25,
                                 yscrollcommand=transaction_scroll.set,
                                 selectmode="extended",
                                 style='Treeview')
        transaction_scroll.config(command=transaction_view.yview)
        transaction_view['columns']=("ITEM","QUANTITY","PRICE")
        transaction_view.column("#0",width=0,stretch = NO)
        transaction_view.column("ITEM", anchor=W,width=250)
        transaction_view.column("QUANTITY", anchor=CENTER, width=75)
        transaction_view.column("PRICE", anchor=E,width=200)
        transaction_view.heading("ITEM", text="ITEM", anchor=W)
        transaction_view.heading("QUANTITY",text="QUANTITY",anchor=CENTER)
        transaction_view.heading("PRICE", text="PRICE", anchor=E)
        transaction_view.pack()


        #CREATE FRAME FOR THE TRANSACTION TOTAL
        # tf=ttk.Style()
        # tf.configure('tf.TFrame',font=(use_font,22),foreground='black',background = "lightblue")
        # total_frame = ttk.Frame(self.root, style='tf.TFrame')
        # total_frame.place(relwidth=frame_rel_width-0.03,relheight =0.1, relx=0.51, rely=0.80)

        #CREATE TRANSACTION LABEL AND TEXTBOX
        subtotal_textbox = ttk.Label(master=transaction_frame,
                                  text="Sub Total     $ 0.00",
                                  foreground = 'black',
                                  background=frame_color,
                                  padding=10,
                                  justify=tk.RIGHT)
        subtotal_textbox.pack(anchor='e')
        tax_textbox = ttk.Label(master=transaction_frame,
                                  text="Tax     $ 0.00",
                                  foreground = 'black',
                                  background=frame_color,
                                  padding=10,
                                  justify=tk.RIGHT)
        tax_textbox.pack(anchor='e')

        total_textbox = ttk.Label(master=transaction_frame,
                                  text="Total     $ 0.00",
                                  foreground = 'black',
                                  background=frame_color,
                                  padding=10,
                                  justify=tk.RIGHT)
        total_textbox.pack(anchor='e')

        checkout_button=tk.Button(master=transaction_frame,
                                  text="CHECKOUT",
                                  foreground='black',
                                  background=frame_color,
                                  padx=20,
                                  pady=20,
                                  font=(use_font,36))
        checkout_button.pack(anchor=CENTER)


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




def showLoginWindow(e):
    e.destroy()
    newRoot=Tk()
    application=LoginWindow.Login(newRoot)
    newRoot.mainloop()

def bakery_frame(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0,weight = 1)
    frame.columnconfigure(1,weight = 3)
    frame['borderwidth'] =5
    frame['relief'] = 'raised'
    return frame


    root.mainloop()


