import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add("*font",('verdana', 20, 'bold'))
        tk.Button(self, text="LEFT",padx=20,pady=20,command=self.left_click).pack(side=tk.LEFT,padx=10,pady=10)
        tk.Button(self, text="CENTER",padx=20,pady=20,command=self.center_click).pack(side=tk.LEFT,padx=10,pady=10)
        tk.Button(self, text="RIGHT",padx=20,pady=20,command=self.right_click).pack(side=tk.LEFT,padx=10,pady=10)

    def left_click(self):
        print("left_click")

    def center_click(self):
        print("center_click")

    def right_click(self):
        print("right_click")


if __name__ == "__main__":
    app = App()
    app.mainloop()

