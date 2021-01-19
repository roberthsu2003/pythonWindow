from tkinter import *
import Pmw
root = Tk()

root.title('Dialog')
Pmw.initialise()

dialog = Pmw.Dialog(root, buttons=('OK', 'Apply', 'Cancel', 'Help'),
	    defaultbutton='OK', title='Simple dialog')

w = Label(dialog.interior(), text='Pmw Dialog\nBring out your dead!',
	    background='black', foreground='white', pady=20)
w.pack(expand=1, fill=BOTH, padx=4, pady=4)
dialog.activate()

root.mainloop()
