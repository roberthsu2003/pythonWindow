import string
from kinter import *
from validation import *


class EntryValidation:
    def __init__(self, master):
        self._ignoreEvent = 0
        self._ipAddrV = self._crdprtV = self._lnameV = ''

        frame = Frame(master)
        Label(frame, text='   ').grid(row=0, column=0, sticky=W)
        Label(frame, text='   ').grid(row=0, column=3, sticky=W)

        self._ipaddr = self.createField(frame, width=15, row=0, col=2,
                                        label='IP Address:', valid=self.validate, enter=self.activate)
        self._crdprt = self.createField(frame, width=8, row=1, col=2,
                                        label='Card - Port:', valid=self.validate, enter=self.activate)
        self._lname = self.createField(frame, width=20, row=2, col=2,
                                       label='Logical Name:', valid=self.validate, enter=self.activate)

        self._wDict = {self._ipaddr: ('_ipAddrV', validIP),
                       self._crdprt: ('_crdprtV', validCP),
                       self._lname: ('_lnameV', validLName)}

        frame.pack(side=TOP, padx=15, pady=15)

    def createField(self, master, label='', text='', width=1,
                    valid=None, enter=None, row=0, col=0):
        Label(master, text=label).grid(row=row, column=col - 1, sticky=W)
        id = Entry(master, text=text, width=width, takefocus=1)
        id.bind('<Any-Leave>', valid)
        id.bind('<FocusOut>', valid)
        id.bind('<Return>', enter)
        id.grid(row=row, column=col, sticky=W)
        return id

    def activate(self, event):
        print
        '<Return>: value is', event.widget.get()

    def validate(self, event):
        if self._ignoreEvent:
            self._ignoreEvent = 0
        else:
            currentValue = event.widget.get()
            if currentValue:
                var, validator = self._wDict[event.widget]
                nValue, replace, valid = validator(currentValue)
                if replace:
                    self._ignoreEvent = 1
                    setattr(self, var, nValue)
                    event.widget.delete(0, END)
                    event.widget.insert(0, nValue)

                if not valid:
                    self._ignoreEvent = 1
                    event.widget.focus_set()


root = Tk()
root.option_add('*Font', 'Verdana 10 bold')
root.option_add('*Entry.Font', 'Courier 10')
root.title('Entry  Validation')

top = EntryValidation(root)
quit = Button(root, text='Quit', command=root.destroy)
quit.pack(side='bottom')

root.mainloop()
