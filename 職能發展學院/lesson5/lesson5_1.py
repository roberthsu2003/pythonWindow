#pack() layout
import tkinter as tk


class Window(tk.Tk):
    def __init__(self,title):
        super().__init__()
        self.title(title)

        tk.Button(self, text="LEFT",padx=10,pady=5).pack(side=tk.LEFT)
        tk.Button(self, text="CENTER",padx=10,pady=5).pack(side=tk.LEFT)
        tk.Button(self, text="RIGHT",padx=10,pady=5).pack(side=tk.LEFT)

if __name__ == "__main__":
    window = Window("layout1")
    window.mainloop()