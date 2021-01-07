from tkinter import *
root = Tk()

class Indicator:
    def __init__(self, master=None, label='', value=0):
        self.var = IntVar()
        self.i = Checkbutton(master, text=label, variable = self.var,
                             command=self.valueChanged)
        self.var.set(value)
        self.i.pack()

    def valueChanged(self):
        print('Current value = %s' % ['Off','On'][self.var.get()])

ind = Indicator(root, label='Furnace On', value=1)
root.mainloop()