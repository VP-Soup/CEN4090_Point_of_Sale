from tkinter import *
from functools import partial
from tkinter import ttk

root = Tk()
root.title("Test")
frame = Frame(root)
frame.grid(column=0, row=0)

# some call to populate an array full of info
items = [("name", "price"), ("name1", "price1"), ]

i = j = 1
for item in items:
    ttk.Button(frame, text=item[0], command=partial(print, item[1])).grid(column=i, row=j, sticky="n,e,s,w")
    if i == 3:
        i = 1
        j += 1
    else:
        i += 1

root.minsize(width=270, height=270)
root.mainloop()
