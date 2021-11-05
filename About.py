##########################################################################################################
## Application Bakery Point of Sale - 3FPS                                                              ##
## Bakery About GUI: provides a little information about the application and the reference sources      ##
##                  used while learning python and tkinter                                              ##
## References: YouTube.com, Codemy.com, Stackoverflow.com, tutorialspoint.com, geeksforgeeks.org,       ##
##            pythonguides.com, anzeljg.github.io, & pythontutorial.net                                 ##
## Date: 06NOV21                                                                                        ##
##########################################################################################################

from tkinter import ttk
import tkinter as tk


class About():
    # DEFINE GLOBAL SETTING FOR ROOT WINDOW WIDTH AND HEIGHT
    global root_width
    root_width = 500
    global root_height
    root_height = 500
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('About Bakery')
        self.root.iconbitmap('CakesBakery.png')

        # GET THE DISPLAY WINDOW DIMENSIONS
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # FIND THE CENTER OF THE MONITOR WINDOW
        window_center_x = int(screen_width / 2 - root_width / 2)
        window_center_y = int(screen_height / 2 - root_height / 2)

        # SET THE ROOT WINDOW LOCATION ON THE DISPLAY
        self.root.geometry(f'{root_width}x{root_height}+{window_center_x}+{window_center_y}')

        about_frame=ttk.Frame(self.root)
        about_frame.pack()

        about_textbox=tk.Label(about_frame,
                                height=500,
                                width=500,
                                text='Bakery Point of Sale Application - Team 3FPS\n'
                                     'This application provides a user interface for mananaging retail sales\n'
                                     'References for this project include:\n'
                                     '\t\tYouTube.com,\n'
                                     '\t\tCodemy.com,\n'
                                     '\t\tStackoverflow.com,\n'
                                     '\t\ttutorialspoint.com,\n'
                                     '\t\tgeeksforgeeks.org,\n'
                                     '\t\tpythonguides.com,\n'
                                     '\t\t anzeljg.github.io,\n'
                                     '\t\t and pythontutorial.net',
                                justify='left',
                                anchor='nw',
                                padx=25,
                                pady=25)
        about_textbox.pack()

        self.root.mainloop()
