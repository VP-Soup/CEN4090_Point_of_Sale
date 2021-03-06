from tkinter import ttk
import tkinter as tk

# Database GUI window for entering products into the database
# References: YouTube.com, Codemy.com, Stackoverflow.com, tutorialspoint.com, geeksforgeeks.org, pythonguides.com
#             anzeljg.github.io, pythontutorial.net

class BakeryButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None,bg_color=None, text="", command=None, style=None):
        ttk.Frame.__init__(self,
                           parent,
                           height=height,
                           width=width)
        self.pack_propagate(0)
        self.button = ttk.Button(self, text=text,command=command)
        self.button.pack(fill=tk.BOTH, expand=1)