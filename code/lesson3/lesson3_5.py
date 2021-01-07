from tkinter import *
import random

root = Tk()


class Indicator:
    def __init__(self, master=None, label='', value=0.0):
        self.var = DoubleVar()
        self.s = Scale(master, label=label, variable=self.var,
                       from_=0.0, to=300.0, orient=HORIZONTAL,
                       length=300)
        self.value = value
        self.var.set(value)
        self.s.pack()
        self.s.after(1000, self.update)

    def set(self, value):
        self.value = value

    def update(self):
        self.var.set(self.value)
        self.s.update_idletasks()
        self.s.after(1000, self.update)


def setTemp():
    slider = random.choice(range(10))
    value = random.choice(range(0, 300))
    slist[slider].set(value)
    root.after(5, setTemp)


slist = []
for i in range(10):
    slist.append(Indicator(root, label='Probe %d' % (i + 1)))

setTemp()
root.mainloop()
