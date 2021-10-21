from PIL import ImageTk
from BakeryWindow import *
from tkinter import *
from tkinter import ttk


class Login:

    # Testing without using the DB
    user = 'admin'
    passw ='admin'

    def __init__(self,root):

        self.root = root
        self.root.title('LOGIN SCREEN')

        # Have to fix image for OOP
        """self.logo = Image.open("CakesBakery.png", )
        self.newLogoSize = ImageTk.PhotoImage(resized)
        self.resized = self.logo.resize((500, 500), Image.ANTIALIAS)
        self.img_label = Label(root, image=self.newLogoSize, borderwidth=0)
        self.img_label.grid(row=0, column=5)"""

        # Username box
        Label(text = ' Username ',font='Times 15').grid(row=1,column=1,pady=20)
        self.username = Entry()
        self.username.grid(row=1,column=2,columnspan=10)

        # Password box
        Label(text = ' Password ',font='Times 15').grid(row=2,column=1,pady=10)
        self.password = Entry(show='*')
        self.password.grid(row=2,column=2,columnspan=10)

        # Login button
        ttk.Button(text='LOGIN',command=self.login_user).grid(row=3,column=2)


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

        else:
            '''Prompt user that either id or password is wrong'''
            self.message = Label(text = 'Username or Password incorrect. Try again!',fg = 'Red')
            self.message.grid(row=6,column=2)
