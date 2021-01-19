from tkinter import *
import Pmw
root = Tk()
root.title('CounterDialog')
Pmw.initialise()

choice = None

dialog = Pmw.CounterDialog(root,
                           label_text = 'Enter the number of twits (2 to 8)\n',
                           counter_labelpos = N,
                           entryfield_value = 2,
                           counter_datatype = 'numeric',
                           entryfield_validate =
                           {'validator' : 'numeric', 'min' : 2, 'max' : 8},
                           buttons = ('OK', 'Cancel'),
                           defaultbutton = 'OK',
                           title = 'Twit of the Year')
dialog.tkraise()

result = dialog.activate()
print('You clicked on', result, dialog.get())

root.mainloop()
