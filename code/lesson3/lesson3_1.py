from tkinter import *

root = Tk()

def enter(event):
    print('Entered Frame: x=%d, y=%d' % (event.x, event.y))

frame = Frame(root, width=150, height=150)
frame.bind('<Any-Enter>', enter)
frame.pack()

root.mainloop()