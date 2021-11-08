from PIL import ImageTk
import PIL.Image
from DataAccess import *
from BakeryWindow import *
from DatabaseWindow import *
from tkinter import *
from tkinter import ttk


class Login:

    # Testing without using the DB
    user = 'user'
    passw ='user'
    adminUser='admin'
    adminPassw='admin'

    def __init__(self,root):

        self.root = root
        self.root.title('LOGIN SCREEN')
        self.root.configure(background='white')
        root_width = 600
        root_height = 600


        # GET THE DISPLAY WINDOW DIMENSIONS
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x = int(screen_width / 2 - root_width / 2)
        window_center_y = int(screen_height / 2 - root_height / 2)

        # SET THE ROOT WINDOW LOCATION ON THE DISPLAY
        root.geometry(f'{root_width}x{root_height}+{window_center_x}+{window_center_y}')

        # Image import
        self.img = PIL.Image.open("CakesBakery.png")
        self.img = self.img.resize((400, 400))
        self.img = ImageTk.PhotoImage(self.img)

        self.img_label = Label(self.root, image=self.img, borderwidth=0)
        self.img_label.pack()

        #FRAME FOR THE LOGIN USERNAME AND PASSWORD
        login_frame=LabelFrame(self.root,background='white')
        login_frame['borderwidth']=0
        login_frame.pack()
        # Username box
        Label(login_frame,text = ' Username ',font='calibre 13',background='white').grid(row=1,column=1,pady=20,)
        self.username = Entry(login_frame)
        self.username.grid(row=1,column=2,columnspan=10)
        self.username.focus_set()

        # Password box
        Label(login_frame,text = ' Password ',font='calibre 13',background='white').grid(row=2,column=1,pady=10)
        self.password = Entry(login_frame,show='*')
        self.password.grid(row=2,column=2,columnspan=10)

        # Login button
        self.login_btn = PIL.Image.open("login_image.png")
        self.login_btn = self.login_btn .resize((100, 50))
        self.login_btn = ImageTk.PhotoImage(self.login_btn)

        # NEED TO FIX Button border to 0

        button_frame=Frame(self.root)
        button_frame.pack()
        self.LoginButton = ttk.Button(button_frame,text='LOGIN',command=self.login_user, image = self.login_btn).pack()

        #IF ENTER IS PRESSED SPECIFICALLY AFTER ENTERING THE PASSWORD ACK LIKE PRESSING THE LOGIN BUTTON
        def callback(event):
            self.login_user()

        # IF ENTER IS PRESSED SPECIFICALLY AFTER ENTERING THE PASSWORD ACK LIKE PRESSING THE LOGIN BUTTON
        root.bind('<Return>',callback)

    def login_user(self):


        # We are getting admin 123
        # -1 - returned from the DAL for "admin" and "123" - should return 1
        # we need to fix this error

        if validateLoginCredentials(self.username.get().encode(),self.password.get().encode()):

            #Do the work done by the main of DBMSproject.py

            #Destroy the current window
            self.root.destroy()

                    #Open new window
            newroot = Tk()
            application = Bakery(newroot)
            newroot.mainloop()
        else:
            '''Prompt user that either id or password is wrong'''
            msg_frame=Frame(self.root)
            msg_frame.pack(anchor=CENTER)
            self.message = Label(text = 'Username or Password incorrect. Try again!',fg = 'Red')
            self.message.pack()
