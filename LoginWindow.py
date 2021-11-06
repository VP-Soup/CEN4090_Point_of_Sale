from PIL import ImageTk
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
        root_width = 350
        root_height = 200


        # GET THE DISPLAY WINDOW DIMENSIONS
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x = int(screen_width / 2 - root_width / 2)
        window_center_y = int(screen_height / 2 - root_height / 2)

        # SET THE ROOT WINDOW LOCATION ON THE DISPLAY
        root.geometry(f'{root_width}x{root_height}+{window_center_x}+{window_center_y}')

        # Have to fix image for OOP
        """self.logo = Image.open("CakesBakery.png", )
        self.newLogoSize = ImageTk.PhotoImage(resized)
        self.resized = self.logo.resize((500, 500), Image.ANTIALIAS)
        self.img_label = Label(root, image=self.newLogoSize, borderwidth=0)
        self.img_label.grid(row=0, column=5)"""

        #FRAME FOR THE LOGIN USERNAME AND PASSWORD
        login_frame=LabelFrame(self.root)
        login_frame['borderwidth']=0
        login_frame.pack()
        # Username box
        Label(login_frame,text = ' Username ',font='Times 15').grid(row=1,column=1,pady=20)
        self.username = Entry(login_frame)
        self.username.grid(row=1,column=2,columnspan=10)
        self.username.focus_set()

        # Password box
        Label(login_frame,text = ' Password ',font='Times 15').grid(row=2,column=1,pady=10)
        self.password = Entry(login_frame,show='*')
        self.password.grid(row=2,column=2,columnspan=10)

        # Login button
        button_frame=Frame(self.root)
        button_frame.pack()
        ttk.Button(button_frame,text='LOGIN',command=self.login_user).pack()

        #IF ENTER IS PRESSED SPECIFICALLY AFTER ENTERING THE PASSWORD ACK LIKE PRESSING THE LOGIN BUTTON
        def callback(event):
            self.login_user()

        # IF ENTER IS PRESSED SPECIFICALLY AFTER ENTERING THE PASSWORD ACK LIKE PRESSING THE LOGIN BUTTON
        root.bind('<Return>',callback)

    def login_user(self):

        '''Check username and password entered are correct'''
        if self.username.get() == self.user and self.password.get() == self.passw:

            # Do the work done by the main of DBMSproject.py

            #Destroy the current window
            self.root.destroy()

                #Open new window
            newroot = Tk()
            application = Bakery(newroot)
            newroot.mainloop()
        #
        elif self.username.get() == self.adminUser and self.password.get() == self.adminPassw:

            #Do the work done by the main of DBMSproject.py

            #Destroy the current window
            self.root.destroy()

                    #Open new window
            newroot = Tk()
            application = DatabaseWindow(newroot)
            newroot.mainloop()
        else:
            '''Prompt user that either id or password is wrong'''
            msg_frame=Frame(self.root)
            msg_frame.pack(anchor=CENTER)
            self.message = Label(text = 'Username or Password incorrect. Try again!',fg = 'Red')
            self.message.pack()
