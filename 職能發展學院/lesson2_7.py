import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add("*font",('verdana', 20, 'bold'))
        topFrame = tk.Frame(self,width=300,height=150,bg="#cccccc")
        #內容
        topFrame.pack(fill=tk.X)

        leftFrame = tk.Frame(self, width=150, height=200, bg="#aaaaaa")
        # 內容
        leftFrame.pack(side=tk.LEFT)

        rightFrame = tk.Frame(self, width=200, height=200, bg="#999999")
        # 內容
        rightFrame.pack(side=tk.LEFT)






if __name__ == "__main__":
    app = App()
    app.mainloop()

