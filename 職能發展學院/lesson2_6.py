import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add("*font",('verdana', 20, 'bold'))
        tk.Button(self, text="Top",padx=20,pady=20).pack(side=tk.LEFT,padx=10,pady=10)
        tk.Button(self, text="Center",padx=20,pady=20).pack(side=tk.LEFT,padx=10,pady=10)
        tk.Button(self, text="Button",padx=20,pady=20).pack(side=tk.LEFT,padx=10,pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()

