import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = tk.Frame(self,bg="#cccccc",borderwidth=2,relief="groove")
        btn1 = tk.Button(topFrame,text="下載1",command=self.btn1Click,padx=20,pady=20)
        btn1.pack(side=tk.LEFT,padx=20,pady=20)

        btn2 = tk.Button(topFrame, text="下載2", command=self.btn2Click, padx=20, pady=20)
        btn2.pack(side=tk.LEFT,padx=20, pady=20)

        btn3 = tk.Button(topFrame, text="下載3", command=self.btn3Click, padx=20, pady=20)
        btn3.pack(side=tk.LEFT, padx=20, pady=20)
        topFrame.pack(padx=20,pady=20)

    def btn1Click(self):
        print("btn1 click")

    def btn2Click(self):
        print("btn2 click")

    def btn3Click(self):
        print("btn3 click")


if __name__ == "__main__":
    root = Window()
    root.title("這是我的視窗")
    root.mainloop()