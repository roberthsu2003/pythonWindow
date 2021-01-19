from tkinter import *


def setHeight(heightStr):
    print(heightStr)

root = Tk()
root.title('Scale')

canvas = Canvas(root, width=50, height=50, bd=0, highlightthickness=0)
canvas.create_polygon(0,0,1,1,2,2, fill='cadetblue', tags='poly')
canvas.create_line(0,0,1,1,2,2,0,0, fill='black', tags='line')
scale = Scale(root, orient=VERTICAL, length=284, from_=0, to=250,
              tickinterval=50, command=lambda h:setHeight(h))
scale.grid(row=0, column=0, sticky='NE')
canvas.grid(row=0, column=1, sticky='NWSE')
scale.set(100)
root.mainloop()