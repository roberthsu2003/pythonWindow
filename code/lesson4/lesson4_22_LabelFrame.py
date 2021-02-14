import tkinter as tk
from tkinter import ttk


# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('LabelFrame Demo')

# label frame
lf = ttk.LabelFrame(
    root,
    text='Alignment')

lf.grid(column=0, row=0, padx=20, pady=20)

alignment = tk.StringVar()

# left radio button
left_radio = ttk.Radiobutton(
    lf,
    text='Left',
    value='left',
    variable=alignment
)
left_radio.grid(column=0, row=0, ipadx=10, ipady=10)

# center radio button
center_radio = ttk.Radiobutton(
    lf,
    text='Center',
    value='center',
    variable=alignment
)

center_radio.grid(column=1, row=0, ipadx=10, ipady=10)

# right alignment radiobutton
right_radio = ttk.Radiobutton(
    lf,
    text='Right',
    value='right',
    variable=alignment
)
right_radio.grid(column=2, row=0, ipadx=10, ipady=10)

root.mainloop()