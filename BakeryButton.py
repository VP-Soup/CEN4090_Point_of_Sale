from tkinter import ttk
import tkinter as tk

# Database GUI window for entering products into the database
# References: YouTube.com, Codemy.com, Stackoverflow.com, tutorialspoint.com, geeksforgeeks.org, pythonguides.com
#             anzeljg.github.io, pythontutorial.net

class BakeryButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None,bg_color=None, text="", command=None, style=None):
        ttk.Frame.__init__(self,
                           parent,
                           foreground=bg_color,
                           height=height,
                           width=width)
        self.pack_propagate(0)
        self._btn = ttk.Button(self, text=text,command=command)
        self._btn.pack(fill=tk.BOTH, expand=1)