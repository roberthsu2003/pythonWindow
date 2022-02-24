import tkinter as tk
import dataSource

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        label = tk.Label(self, text="Hello World!")
        label.pack(fill=tk.BOTH, expand=1, padx=100, pady=50)


if __name__ == "__main__":
    dataSource.download_save_to_DataBase()
    window = Window()
    window.title("PM2.5")
    window.mainloop()