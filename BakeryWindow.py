from tkinter import *
import tkinter
import tkinter as tk
from functools import partial
from tkinter import ttk
import sqlite3
from operator import itemgetter
import sys
import DataAccess
import ViewDatabase,Transaction

# Bakery GUI window
# CONSTANT VARIABLES USED THROUGHOUT THE CODE
# FRAME RELATIVE HEIGHT, RELATIVE WIDTH AND A COMMON COLOR
frame_rel_height = 0.9
frame_rel_width = 0.5
frame_color="#eae1df"
button_bg_color = "#f1b0a2"
category_bg_color=["#eba994","#e39888","#94a9eb","#94ebb8","#e7eb94"]
class Bakery:

    def __init__(self, root):
        self.root = root
        self.root.title('Bakery')
        self.scrollable_Button_Frame=ttk.Frame()
        self.create_main_window()


# BUTTON FRAME: CREATE A SCROLLABLE WINDOW TO SCROLL THE PRODUCT BUTTONS.
    def create_button_frame(self):
        bf = ttk.Style()
        bf.configure('new.TFrame', background='white', borderwidth=0, relief='flat')
        button_frame = ttk.Frame(self.root, style='new.TFrame')
        button_frame_label = LabelFrame(button_frame, text="PRODUCT SELECTION", font=('Helvetica', 24))
        button_frame.place(relwidth=frame_rel_width, relheight=frame_rel_height, relx=0.0, rely=0.1)

        button_canvas = tk.Canvas(button_frame)
        button_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar = ttk.Scrollbar(button_frame, orient="vertical", command=button_canvas.yview)

        sbf = ttk.Style()
        sbf.configure('sbf.TFrame', background=frame_color, font=('Helvetica', 20), borderwidth=5,
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
        product_category_names.append("admin")


# MAIN WINDOW DIMENSIONS
# ROOT STYLE SETTING FONT TO HELVETICA AND SIZE 20
        self.root.geometry = ('1920x1080')
        r=ttk.Style()
        r.theme_use('default')
        r.configure('.',background=button_bg_color,font=('Helvetica',20))
        canvas = tk.Canvas(master =self.root, width=1920, height=1080,bg = 'white')
        canvas.pack()


# CREATE THE SCROLLABLE FRAME FOR THE PRODUCT SELECTION BUTTONS TO BE PLACED.
        scrollable_Button_Frame=self.create_button_frame()

# ADD THE HEADER
        appName_Frame = LabelFrame(self.root, text="", background=frame_color)
        appName_Frame['borderwidth']=5
        appName_Frame['relief']='raised'
        appName_Frame.place(relwidth=1.0, relheight=.1, relx=0, rely=0)

        appName = ttk.Label(appName_Frame, text="Bakery", font='Helvetica 24 bold', background = frame_color)
        appName.pack()


# THESE BUTTONS ADDED TO THE HEADER WILL ALLOW FOR EITHER SELECTION BY PRODUCT TYPE OR ALPHABETICAL OR
# SOME OTHER MEANS TO QUICKLY CHOOSE A CATEGORY, QUERY THE DATABASE TO GET THE PRODUCT CATEGORY TYPES AND PUSH THOSE
# TO THE TOP HEADER FOR QUICK LINKS
        for cat in product_category_names:
            ttk.Button(appName_Frame,text=cat,command=lambda cat=cat, data=product_Data: self.assign_product_buttons(cat,data,"scrollable_button_frame")).pack(side=LEFT,padx=10,expand=True)



# transaction FRAME: ADD THE transaction FRAME TO THE RIGHT HALF OF THE SCREEN AND USE 90% OF THE SCREEN HEIGHT (HEADER IS THE
# OTHER 10%)
        rf=ttk.Style()
        rf.configure('transaction.TFrame',background=frame_color, font=('Helvetica',20)) # #7AC5CD
        transaction_frame = ttk.Frame(self.root,style='transaction.TFrame')
        transaction_frame['borderwidth']=5
        transaction_frame['relief']='raised'
        transaction_frame.place(relwidth = frame_rel_width, relheight = frame_rel_height,relx=0.5,rely=0.1)


#transaction FRAME STYLE
        rfs = ttk.Style()
        rfs.theme_use('default')
        rfs.configure("TreeView", background = frame_color, foreground = "black", rowheight = 200,
                        fieldbackground = frame_color, font=('Helvetica', 30)) # #D3D3D3
        rfs.map('TreeView', background =[('selected',"#ab90cb")])
    # ADD SCROLLBAR TO SCROLL THE transaction
        transaction_scroll=Scrollbar(transaction_frame)
        transaction_scroll.pack(side=RIGHT,fill=Y)
        transaction=ttk.Treeview(transaction_frame,height=25, yscrollcommand=transaction_scroll.set, selectmode="extended",style='Treeview')
        transaction_scroll.config(command=transaction.yview)
        transaction['columns']=("ITEM","PRICE")
        transaction.column("#0",width=0,stretch = NO)
        transaction.column("ITEM", anchor=W,width=400)
        transaction.column("PRICE", anchor=E,width=400)
        transaction.heading("ITEM", text="ITEM", anchor=W)
        transaction.heading("PRICE", text="PRICE", anchor=E)
        transaction.pack()
        transaction.tag_configure('oddrow',background="white")
        transaction.tag_configure('evenrow',background="lightblue")


#CREATE FRAME FOR THE TRANSACTION TOTAL
        # tf=ttk.Style()
        # tf.configure('tf.TFrame',font=('Helvetica',22),foreground='black',background = "lightblue")
        # total_frame = ttk.Frame(self.root, style='tf.TFrame')
        # total_frame.place(relwidth=frame_rel_width-0.03,relheight =0.1, relx=0.51, rely=0.80)

#CREATE TRANSACTION LABEL AND TEXTBOX
        total_textbox = ttk.Label(master=transaction_frame,text="Sub Total     $ 0.00", foreground = 'black', background=frame_color)
        total_textbox.pack(anchor='e')
        total_textbox = ttk.Label(master=transaction_frame,text="Tax     $ 0.00", foreground = 'black', background=frame_color)
        total_textbox.pack(anchor='e')
        total_textbox = ttk.Label(master=transaction_frame,text="Total     $ 0.00", foreground = 'black', background=frame_color)
        total_textbox.pack(anchor='e')
        total_textbox = ttk.Label(master=transaction_frame,text=" ", foreground = 'black', background=frame_color)
        total_textbox.pack(anchor='e')
        total_textbox = ttk.Label(master=transaction_frame,text=" ", foreground = 'black', background=frame_color)
        total_textbox.pack(anchor='e')
        total_textbox = ttk.Label(master=transaction_frame,text=" ", foreground = 'black', background=frame_color)
        total_textbox.pack(anchor='e')
        checkout_button=tk.Button(master=transaction_frame,text="CHECKOUT",foreground='black',background=frame_color,padx=20,pady=20,font=('Helvetica',36))
        checkout_button.pack(anchor=CENTER)


# CREATE A BUTTON FOR PRODUCT SELECTION
        psb = ttk.Style()
        psb.configure('b.TButton',font=('Helvetica',20),background=button_bg_color,foreground='black')

        for productID, name, quan, cost, price, cat in product_Data:
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
            #THE COMMENTED LLNNES BELOW ARE FOR DIFFERENT TYPES OF BUTTONS TO BE EXPERIMENTED WITH LATER
            #THE BUTTONS PROVIDE A MORE MODERN LOOK THAN THE REGULAR SQUARE TYPE THAT IS AVAILABLE IN TKINTER
            # selection_button=RoundedButton(button_frame,width=150,height=85, cornerradius=10,padding=0,color='lightblue',
            #                                  bg='white',command=lambda name=name, price=price: transaction.insert(parent='',
            #                                  index='end', text='',values=(name, price)))

            # selection_button = newButton(scrollable_Button_Frame, width=150, height=85, text=name,
            #                              command=lambda name=name, price=price:
            #                              receipt.insert(parent='',index='end', text='',values=(name, price)))\
                # .grid(row=j + 1,column=i, sticky="NESW", padx=10,pady=10)
            selection_button=MyButton(scrollable_Button_Frame,height = 100,width=235,text=name,bg_color=bg_color,
                                      command=lambda name=name,price=price: transaction.insert
                                      (parent='', index='end', text='', values=(name, price)))
            selection_button.grid(row=j + 1,column=i, sticky="NESW", padx=20,pady=20)
            if i == 2:
                i = 0
                j += 1
            else:
                i += 1


#CLASS NEW BUTTON IS TO DRAW A BUTTON FROM INDIVIDUAL LINES THAT WILL ALLOW THE BUTTON TO HAVE A SHADED APPEARANCE
#WILL CONTINUE WORKING ON ONCE OTHER ITEMS ARE FINISHED
class newButton(tk.Canvas):
    def __init__(self,parent, width=None ,height=None, text=None, cornerradius=None, padding = 10, color='', command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, relief='flat')
        bc=tk.Canvas(self,height=100,width=200)
        self.command=command
        self.text=text
        h = 100
        def shaded_button():
            for i in range(1, h):
                redValue = hex(75 - int(i/2))
                blueValue = hex(90 + i)
                greenValue = hex(100 - int(i/2))
                l_color = '#'+redValue+blueValue+greenValue
                h_color=l_color.replace("0x","")
                l_row_local=100-i
                self.create_line(10,l_row_local,210,l_row_local,width=2,fill=h_color)

        id=shaded_button()
        print("Color: ", color)
        self.text_label = tkinter.Label(master=self, text=self.text, font=('Helvetica', 20))
        self.text_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        (x0, y0, x1, y1) = self.bbox("all")
        width = (x1 - x0)
        height = (y1 - y0)
        self.set_text=text
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()


##########################################################################################################
## class RoundedButton(tk.Canvas)                                                                       ##
## Description: creates a rounded button in the forground of color x with a square background color y   ##
##              make the background color the same as the 'canvas' and a rounded buttonn is what        ##
##              displayed                                                                               ##
## Created by : User - Guac, March 6, 2020, thread answer #10                                           ##
##              https://stackoverflow.com/questions/42579927/rounded-button-tkinter-python/45536589     ##
##########################################################################################################
class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0,
            relief="flat", highlightthickness=0, bg=bg)
        self.command = command


        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2*cornerradius
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)


        id = shape()
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()


class MyButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None,bg_color=None, text="", command=None, style=None):
        mb=ttk.Style()
        mb.configure('MyButton.TFrame', font=('Helvetica', 20), background=bg_color, foreground='black',anchor='N')
        ttk.Frame.__init__(self, parent, height=height, width=width, style="MyButton.TFrame")

        self.pack_propagate(0)
        self._btn = ttk.Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=tk.BOTH, expand=1)



def bakery_frame(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0,weight = 1)
    frame.columnconfigure(1,weight = 3)
    frame['borderwidth'] =5
    frame['relief'] = 'raised'
    return frame


    root.mainloop()


