import time, string
from tkinter import *
import Pmw


class EntryValidation:
    def __init__(self, master):
        now = time.localtime(time.time())
        self._date = Pmw.EntryField(master,
                                    labelpos='w', label_text='Date (yy/mm/dd):',
                                    value='%d/%d/%d' % (now[0], now[1], now[2]),
                                    validate={'validator': 'date', 'separator': '/'})
        self._time = Pmw.EntryField(master,
                                    labelpos='w', label_text='Time (24hr clock):',
                                    value='8:00:00',
                                    validate={'validator': 'time',
                                              'min': '00:00:00', 'max': '23:59:59',
                                              'minstrict': 0, 'maxstrict': 0})
        self._real = Pmw.EntryField(master,
                                    labelpos='w', value='127.2',
                                    label_text='Real (50.0 to 1099.0):',
                                    validate={'validator': 'real',
                                              'min': 50, 'max': 1099,
                                              'minstrict': 0},
                                    modifiedcommand=self.valueChanged)
        self._ssn = Pmw.EntryField(master,
                                   labelpos='w', label_text='Social Security #:',
                                   validate=self.validateSSN, value='')

        fields = (self._date, self._time, self._real, self._ssn)

        for field in fields:
            field.pack(fill='x', expand=1, padx=12, pady=8)
        Pmw.alignlabels(fields)

        self._date.component('entry').focus_set()

    def valueChanged(self):
        print('Value changed, value is', self._real.get())


    def validateSSN(self, contents):
        result = -1
        if '-' in contents:
            ssnf = string.splitfields(contents, '-')
            try:
                if len(ssnf[0]) == 3 and \
                        len(ssnf[1]) == 2 and \
                        len(ssnf[2]) == 4:
                    result = 1
            except:
                result = -1
        else:
            if len(contents) == 9:
                result = 1
        return result


######################################################################

if __name__ == '__main__':
    root = Tk()
    root.option_add('*Font', 'Verdana 10 bold')
    root.option_add('*EntryField.Entry.Font', 'Courier 10')
    root.option_add('*EntryField.errorbackground', 'yellow')
    Pmw.initialise(root, useTkOptionDb=1)
    root.title('Pmw EntryField Validation')

    quit = Button(root, text='Quit', command=root.destroy)
    quit.pack(side='bottom')
    top = EntryValidation(root)
    root.mainloop()
