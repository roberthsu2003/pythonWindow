#pack() layout
import tkinter as tk


class Window(tk.Tk):
    def __init__(self,title):
        super().__init__()
        self.title(title)
        self.option_add('*font',('verdana',20))
        fm = tk.Frame(self,bg="#aaaaaa")
        tk.Button(fm, text="LEFT",padx=10,pady=5).pack()
        tk.Button(fm, text="This is the Center Button",padx=10,pady=5).pack()
        tk.Button(fm, text="RIGHT",padx=10,pady=5).pack()
        fm.pack()

if __name__ == "__main__":
    window = Window("layout1")
    window.mainloop()