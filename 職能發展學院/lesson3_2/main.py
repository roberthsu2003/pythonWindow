import tkinter as tk
import dataSource

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        print(dataSource.DATA)
        titleFrame = tk.Frame(self, bg="#333333",borderwidth=2,relief=tk.SUNKEN,padx=50,pady=50)
        tk.Label(titleFrame,text="台北市youbike2.0即時資訊",bg="#333333",fg="#cccccc",font=('arial',20)).pack()
        updateButton = tk.Button(titleFrame,text="立即更新",bg="#333333",fg="#333333",font=('arial',16),command=lambda :dataSource.download())
        updateButton.pack(pady=(20,0))
        titleFrame.pack(pady=20)

        col = 4
        for i in range(len(dataSource.AREA)):
            if  i % col == 0:
                topFrame = tk.Frame(self, bg="#cccccc", borderwidth=2, relief="groove")
                topFrame.pack(padx=20, pady=20)
            areaName = dataSource.AREA[i]
            btn1 = tk.Button(topFrame, text=areaName, padx=20, pady=20,command=lambda :self.areaClick(areaName))
            btn1.pack(side=tk.LEFT, padx=20, pady=20)

    def areaClick(self,areaName):
        print(areaName)


if __name__ == "__main__":
    root = Window()
    root.title("這是我的視窗")
    root.mainloop()