import tkinter as tk
from datasource import populations

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("上課作業")
        self.option_add("*font",("verdana", 20))
        #self.geometry("300x200")

        tk.Label(self,text="三個功能按鈕").pack(pady=20)
        topFrame = tk.Frame(self,bg="#aaaaaa")
        tk.Button(topFrame,text="台灣總人口數",padx=5,pady=5).pack(side=tk.LEFT,expand=tk.YES,padx=(20,10),pady=(10,20))
        tk.Button(topFrame,text="台灣總土地",padx=5,pady=5).pack(side=tk.LEFT,expand=tk.YES,padx=(10,10),pady=(10,20))
        tk.Button(topFrame,text="台灣總區鄉鎮數",padx=5,pady=5).pack(side=tk.LEFT,expand=tk.YES,padx=(10,20),pady=(10,20))
        topFrame.pack(expand=tk.YES,fill=tk.BOTH)

if __name__ == "__main__":
    for item in populations:
        print(item[1])
    window = Window()
    window.mainloop()