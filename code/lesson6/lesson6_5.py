from tkinter import *


class Var(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.field = Entry()
        self.field.pack()

        self.value = StringVar()
        self.value.set("Jean-Paul Sartre")
        self.field["textvariable"] = self.value

        self.field.bind('<Key-Return>', self.print_value)

    def print_value(self, event):
        print('Value is "%s"' % self.value.get())


test = Var()
test.mainloop()