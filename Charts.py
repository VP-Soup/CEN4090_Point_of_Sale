##########################################################################################################
## Application Bakery Point of Sale - 3FPS                                                              ##
## Bakery Charts GUI: interface with the products datatable to provide a visual indication of some of   ##
##                  the key sales metrics a business may want available                                 ##
## References: YouTube.com, Codemy.com, Stackoverflow.com, tutorialspoint.com, geeksforgeeks.org,       ##
##            pythonguides.com, anzeljg.github.io, & pythontutorial.net                                 ##
## Date: 06NOV21                                                                                        ##
##########################################################################################################

from tkinter import *
from tkinter import ttk

import About,BakeryWindow,BakeryButton
import Charts


class Graph():
    # global root_width
    # root_width = 1900
    # global root_height
    # root_height = 1000

    #DUMMY FUNCTION- DOES NOTHING
    def doNothing():
        pass

    #SHOW THE MAIN WINDOW - BAKERY WINDOW
    def showBakeryWindow(e,eid):
        e.destroy()
        newRoot = Tk()
        application = BakeryWindow.Bakery(newRoot, eid)
        newRoot.mainloop()

    def __init__(self,root, eid):
        self.root = root
        self.root.title("PRODUCT SALES PERFORMANCE")
        self.eid = eid
        # GET THE DISPLAY WINDOW DIMENSIONS
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x = int(screen_width / 2 - screen_width / 2)
        window_center_y = int(screen_height / 2 - screen_height / 2)

        # FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x = int(screen_width / 2 - screen_width / 2)
        window_center_y = int(screen_height / 2 - screen_height / 2)

        # SET THE ROOT WINDOW LOCATION ON THE DISPLAY
        root.geometry(f'{screen_width}x{screen_height}+{window_center_x}+{window_center_y}')

        # CREATE A MENU BAR
        app_menu = Menu(root)

        # FILE MENU ITEMS
        file_menu = Menu(app_menu, tearoff=0)
        # file_menu.add_command(label="New", )
        # file_menu.add_command(label="Open", )
        # file_menu.add_command(label="Save", )
        # file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        app_menu.add_cascade(label="File", menu=file_menu)

        # ADMINISTRATOR MENU OPTIONS
        admin_menu = Menu(app_menu, tearoff=0)
        admin_menu.add_command(label="Login", command=lambda: BakeryWindow.showLoginWindow(root))
        admin_menu.add_command(label="Logout", command=lambda: BakeryWindow.Bakery(root, self.eid))
        admin_menu.add_separator()
        admin_menu.add_command(label="Charts", command=Graph.doNothing())
        app_menu.add_cascade(label="Admin", menu=admin_menu)

        # HELP MENU OPTIONS
        help_menu = Menu(app_menu, tearoff=0)
        help_menu.add_command(label="Help", )
        help_menu.add_command(label="About", command=About.About)
        app_menu.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=app_menu)


        button_width = 250
        button_height = 75

        #CREATE A FRAME ON THE LEFT SIDE OF THE WINDOW TO PROVIDE A COLUMN OF BUTTONS
        #FOR CHART SELECTION
        # CREATE A NEW FRAME TO ADD THE RECORD ENTRY AND DELETE BUTTONS
        db_button_frame = LabelFrame(root, text="CHARTS")
        db_button_frame.grid(row=0,column=0, padx=10, pady=10,sticky=N)

        update_button = BakeryButton.BakeryButton(db_button_frame,
                                                  height=button_height,
                                                  width=button_width,
                                                  text="TOP 10 PRODUCTS",command=lambda: topTenSellers())
        update_button.pack()

        add_records_button = BakeryButton.BakeryButton(db_button_frame,
                                                       height=button_height,
                                                       width=button_width,
                                                       text="HIGHEST SALES MONTH",command=Graph.doNothing())
        add_records_button.pack()

        remove_record_button = BakeryButton.BakeryButton(db_button_frame,
                                                         height=button_height,
                                                         width=button_width,
                                                         text="",command=Graph.doNothing())
        remove_record_button.pack()

        remove_all_button = BakeryButton.BakeryButton(db_button_frame,
                                                      height=button_height,
                                                      width=button_width,
                                                      text="",command=Graph.doNothing())
        remove_all_button.pack()

        move_up_button = BakeryButton.BakeryButton(db_button_frame,
                                                   height=button_height,
                                                   width=button_width,
                                                   text="",command=Graph.doNothing())
        move_up_button.pack()

        move_down_button = BakeryButton.BakeryButton(db_button_frame,
                                                     height=button_height,
                                                     width=button_width,
                                                     text="",command=Graph.doNothing())
        move_down_button.pack()

        select_button = BakeryButton.BakeryButton(db_button_frame,
                                                  height=button_height,
                                                  width=button_width,
                                                  text="", command=Graph.doNothing())
        select_button.pack()

        exit_button = BakeryButton.BakeryButton(db_button_frame,
                                                height=button_height,
                                                width=button_width,
                                                text="EXIT", command=lambda: Graph.showBakeryWindow(self.root, self.eid))
        exit_button.pack()

        db_button_frame_width=db_button_frame.winfo_width()

        #CREATE THE BAR GRAPH FRAME
        bar_graph_frame=ttk.LabelFrame(root,text="Bar Graph")
        bar_graph_frame.grid(row=0,column=1,padx=10, pady=10,sticky=N)

        #CREATE A CANVAS TO DRAW THE GRAPH INTO
        bar_graph_canvas_width=(screen_width-db_button_frame_width-50)
        bar_graph_canvas_height=(screen_height/0.75)
        bar_graph_canvas=Canvas(bar_graph_frame,
                                width=bar_graph_canvas_width,
                                height=bar_graph_canvas_height,
                                #padding=20,
                                bg='white')
        bar_graph_canvas['borderwidth']=15
        bar_graph_canvas.pack()

        bar_graph_y_height=400                      # MAXIMUM HEIGHT OF GRAPH
        bar_graph_y_gap=100                         # SPACE ABOVE
        bar_graph_bar_width=100                     # WIDTH OF BAR
        bar_graph_x_gap=20                          # SPACE BETWEEN THE GRAPH BARS




        def topTenSellers():
            #get sql data for the top 10 or x number of products

            # NEED TO GET THE MAXIMUM VALUES FROM THE DATABASE
            bakery_data = [10, 19, 2, 45, 6, 5]

            # GET THE DATA TO BE GRAPHED
            # ENUMERATE THE DATA TO GET THE MAXIMUM VALUE TO BE THE SPAN OF THE Y-AXIS
            # CREATE THE BAR WIDTHS AND HEIGHT FOR THE DATA TO GRAPH
            for x, y in enumerate(bakery_data):
                max_value = max(bakery_data)
                x0=x*bar_graph_bar_width+x*bar_graph_bar_width+bar_graph_x_gap
                #y0=(bar_graph_y_height*y/max_value)-bar_graph_y_gap
                y0=bar_graph_y_height
                x1=x*bar_graph_bar_width+x*bar_graph_bar_width+bar_graph_bar_width+bar_graph_x_gap
                y1=bar_graph_y_height-(bar_graph_y_height*y/max_value)
                bar_graph_canvas.create_rectangle(x0,y0,x1,y1,fill='grey')
                bar_graph_canvas.create_text(x0+bar_graph_bar_width/2,
                                             bar_graph_y_height+50,
                                             anchor=S,
                                             text="test",
                                             font=('Times',18,'bold'))
                bar_graph_canvas.create_text(x0 + bar_graph_bar_width / 2,
                                             bar_graph_y_height+75,
                                             anchor=S,
                                             text=y,
                                             font=('Times', 18, 'bold'))

        root.mainloop()