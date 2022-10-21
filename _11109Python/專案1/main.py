import tkinter as tk


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("這是我的第一個觀窗")
        btn = tk.Button(self,text="請按我",padx=20,pady=20,font=('arial',16))
        btn.pack(padx=50,pady=30)


def main():
    window = Window()
    window.mainloop()

if __name__ == "__main__":
    main()