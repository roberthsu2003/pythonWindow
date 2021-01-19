from tkinter import *

root = Tk()
root.title('Listbox')
list = Listbox(root, width=15)
list.pack()
for item in range(10):
    list.insert(END, item)
root.mainloop()
