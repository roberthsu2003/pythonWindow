import tkinter as tk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


def main():
    window = Window()
    window.title("這是第一個視窗")
    window.geometry("400x300")
    window.mainloop()

if __name__ == "__main__":
    main()