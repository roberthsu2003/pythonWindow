import tkinter as tk
import dataSource

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = tk.Frame(self,bg="#cccccc",borderwidth=2,relief="groove")
        i = 0
        for area in dataSource.AREA:
            if i == 0:
                topFrame = tk.Frame(self, bg="#cccccc", borderwidth=2, relief="groove")
                topFrame.pack(padx=20, pady=20)
            btn1 = tk.Button(topFrame, text=area, command=self.btn1Click, padx=20, pady=20)
            btn1.pack(side=tk.LEFT, padx=20, pady=20)
            i += 1
            if i == 4:
                i=0





    def btn1Click(self):
        youbikeList =dataSource.download()
        for site in youbikeList:
            print(site)

    def btn2Click(self):
        print("btn2 click")

    def btn3Click(self):
        print("btn3 click")


if __name__ == "__main__":
    root = Window()
    root.title("這是我的視窗")
    root.mainloop()