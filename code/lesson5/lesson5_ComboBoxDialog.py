from tkinter import *
import Pmw
root = Tk()

root.title('ComboBoxDialog')
Pmw.initialise()

choice = None

def choseEntry(entry):
    print('You chose "%s"' % entry)
    choice.configure(text=entry)

plays = ("The Taming of the Shrew", "Two Gentelmen of Verona", "Twelfth Night", "The Merchant of Venice", "Hamlet", "King Richard the Third")

dialog = Pmw.ComboBoxDialog(root, title = 'ComboBoxDialog',
	    buttons=('OK', 'Cancel'), defaultbutton='OK',
	    combobox_labelpos=N, label_text='Which play?',
	    scrolledlist_items=plays, listbox_width=22)
dialog.tkraise()

result = dialog.activate()
print('You clicked on', result, dialog.get())

root.mainloop()
