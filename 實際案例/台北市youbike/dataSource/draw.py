import tkinter as tk

#建立有顏色的3個小圓點的canvas
def getInfoCanvas(parent):
    infoCanvas=tk.Canvas(parent,width=200,height=100,bg='#ffffff')
    infoCanvas.create_oval(10,10,30,30,fill='red')
    infoCanvas.create_text(70,20,text='已無車',font=('Arial',13,'bold'))
    infoCanvas.create_oval(10,40,30,60,fill='orange')
    infoCanvas.create_text(70, 50, text='快沒車', font=('Arial', 13, 'bold'))
    infoCanvas.create_oval(10,70, 30,90, fill='green')
    infoCanvas.create_text(70, 80, text='車很多', font=('Arial', 13, 'bold'))
    return infoCanvas

#建立有顏色的小圓點的canvas
def getColorCircle(parent,color):
    circleCanvas=tk.Canvas(parent,width=40,height=40,bg='#cccccc',highlightthickness=0)
    circleCanvas.create_oval(10, 10, 30, 30, fill=color)
    return circleCanvas