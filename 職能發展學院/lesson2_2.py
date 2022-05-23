import tkinter as tk
import tkinter.font as tkFont

def main():
    window = tk.Tk()
    window.title("這是我的第一個視窗")
    window.geometry("300x300")
    window.resizable(width=0, height=0)
    font=tkFont.Font(family="Lucida Grande", size=20)
    label = tk.Label(window,text="這是我的第一個視窗",bg="#cccccc",font=font)
    label.pack(fill="x")
    window.mainloop()

if __name__ == "__main__":
    main()

