from tkinter import *
import Pmw
root = Tk()
root.title('Balloon Help')
Pmw.initialise()

balloon = Pmw.Balloon(root)

frame = Frame(root)
frame.pack(padx = 10, pady = 5)
field = Pmw.EntryField(frame, labelpos=W, label_text='Name:')
field.setentry('A.N. Other')
field.pack(side=LEFT, padx = 10)
balloon.bind(field, 'Your name', 'Enter your name')

check = Button(frame, text='Check')
check.pack(side=LEFT, padx=10)
balloon.bind(check, 'Look up', 'Check if name is in the database')

frame.pack()

messageBar = Pmw.MessageBar(root, entry_width=40,
                            entry_relief=GROOVE,
                            labelpos=W, label_text='Status:')
messageBar.pack(fill=X, expand=1, padx=10, pady=5)

balloon.configure(statuscommand = messageBar.helpmessage)

root.mainloop()
