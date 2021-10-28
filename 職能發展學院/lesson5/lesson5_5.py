import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("上課作業")
        self.option_add("*font",("verdana", 20))
        self.geometry("300x200")

        tk.Label(self,text="三個功能按鈕").pack(pady=20)
        topFrame = tk.Frame(self,bg="#aaaaaa")
        tk.Button(topFrame,text="LEFT").pack(side=tk.LEFT,expand=tk.YES)
        tk.Button(topFrame,text="CENTER").pack(side=tk.LEFT,expand=tk.YES)
        tk.Button(topFrame,text="RIGHT").pack(side=tk.LEFT,expand=tk.YES)
        topFrame.pack(expand=tk.YES,fill=tk.BOTH)

if __name__ == "__main__":
    window = Window()
    window.mainloop()