from tkinter import *
import Pmw, time

root = Tk()
root.title('Counter')
Pmw.initialise()


def execute(self):
    print('Return pressed, value is', date.get())


date = Pmw.Counter(root, labelpos=W,
                   label_text='Date (4-digit year):',
                   entryfield_value=time.strftime('%d/%m/%Y',
                                                  time.localtime(time.time())),
                   entryfield_command=execute,
                   entryfield_validate={'validator': 'date', 'format': 'dmy'},
                   datatype={'counter': 'date', 'format': 'dmy', 'yyyy': 1})
real = Pmw.Counter(root, labelpos=W,
                   label_text='Real (with comma):',
                   entryfield_value='1,5',
                   datatype={'counter': 'real', 'separator': ','},
                   entryfield_validate={'validator': 'real',
                                        'min': '-2,0', 'max': '5,0',
                                        'separator': ','},
                   increment=.1)
int = Pmw.Counter(root, labelpos=W,
                  label_text='Integer:',
                  orient=VERTICAL,
                  entry_width=2,
                  entryfield_value=50,
                  entryfield_validate={'validator': 'integer',
                                       'min': 0, 'max': 99})

counters = (date, real)
Pmw.alignlabels(counters)

for counter in counters:
    counter.pack(fill=X, expand=1, padx=10, pady=5)
    int.pack(padx=10, pady=5)

root.mainloop()