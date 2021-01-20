from tkinter import *
from tkinter.simpledialog import askinteger
import Pmw

class App:
    def __init__(self, master):
        self.result = Pmw.EntryField(master, entry_width=8,
                                     value='',
                                     label_text='Returned value:  ',
                                     labelpos=W, labelmargin=1)
        self.result.pack(padx=15, pady=15)

root = Tk()
display = App(root)

retVal = askinteger("The Larch",
                    "What is the number of The Larch?",
                    minvalue=0, maxvalue=50)
display.result.setentry(retVal)

root.mainloop()