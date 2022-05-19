from tkinter import Tk,Canvas

class RedBall(Canvas):
    def __init__(self,master,**kw):
        super().__init__(master=master,**kw)
        self.configure(width=20)
        self.configure(height=20)
        self.create_oval(5,5,15,15,fill='#333333')

class Window(Tk):
    def __init__(self):
        super().__init__()
        redball = RedBall(self)
        redball.pack()

if __name__ == "__main__":
    root = Window()
    root.title("自訂類別")
    root.mainloop()
