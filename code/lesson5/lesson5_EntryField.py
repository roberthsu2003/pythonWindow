from tkinter import *
import Pmw
root = Tk()

root.title('EntryField')
Pmw.initialise()

noval = Pmw.EntryField(root, labelpos=W, label_text='No validation',
		validate = None)
real  = Pmw.EntryField(root, labelpos=W,	value = '98.4',
		label_text = 'Real (96.0 to 107.0):',
		validate = {'validator' : 'real',
			'min' : 96, 'max' : 107, 'minstrict' : 0})
int   = Pmw.EntryField(root, labelpos=W, label_text = 'Integer (5 to 42):',
		validate = {'validator' : 'numeric',
			'min' : 5, 'max' : 42, 'minstrict' : 0},
		value = '12')
'''

date = Pmw.EntryField(root, labelpos=W,	label_text = 'Date (in 2000):',
		value = '2000/1/1', validate = {'validator' : 'date',
			'min' : '2000/1/1', 'max' : '2000/12/31',
			'minstrict' : 0, 'maxstrict' : 0,
			'format' : 'ymd'})
'''
widgets = (noval, real, int,)

for widget in widgets:
    widget.pack(fill=X, expand=1, padx=10, pady=5)
Pmw.alignlabels(widgets)
real.component('entry').focus_set()

root.mainloop()