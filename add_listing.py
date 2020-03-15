from tkinter import *

from tkinter import font

from tkinter.ttk import *

import sys

def clicked():
    window.attributes("-topmost", False)
    window2 = Tk()
    window2.attributes("-topmost", True)

    label = Label(window2, text="Successfully added item to the database!")
    label.pack()

    button = Button(window2, text="Ok", command=sys.exit)
    button.pack()

window = Tk()
# window.geometry('350x200')

default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=16)

entry_font = font.nametofont("TkTextFont")
entry_font.configure(size=16)

caption_font = font.nametofont("TkCaptionFont")
caption_font.configure(size=16)

product_name_label = Label(window, text="Product name")
product_name_label.grid(column=0, row=0)

product_name_entry = Entry(window, width=20)
product_name_entry.grid(column=1, row=0)

category_label = Label(window, text="Item category")
category_label.grid(column=0, row=1)

category_entry = Combobox(window, values=[
    "Furniture",
    "Tools",
    "Electronics",
    "Clothing",
    "Instruments",
    "Other"
], state="readonly", font=default_font)
category_entry.grid(column=1, row=1)

condition_label = Label(window, text="Condition")
condition_label.grid(column=0, row=2)

condition_entry = Combobox(window, values=[
    "New",
    "Mint",
    "Excellent",
    "Very Good",
    "Good",
    "Fair",
    "Needs Work"
], state="readonly")
condition_entry.grid(column=1, row=2)

address_label = Label(window, text="Address")
address_label.grid(column=0, row=3)

address_entry = Entry(window, width=20)
address_entry.grid(column=1, row=3)

image_label = Label(window, text="Image")
image_label.grid(column=0, row=4)

image_entry = Entry(window, width=20)
image_entry.grid(column=1, row=4)

description_label = Label(window, text="Description")
description_label.grid(column=0, row=5)

description_entry = Text(window, width=20, height=5, borderwidth=2, relief=RIDGE)
description_entry.grid(column=1, row=5)

btn = Button(window, text="Submit", command=clicked)
btn.grid(column=0, row=6)

product_name_entry.focus()

window.attributes("-topmost", True)
window.focus_force()
window.mainloop()
