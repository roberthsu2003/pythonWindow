import tkinter as tk
import tkinter.font as tkFont

def main():
    window = tk.Tk()
    window.title("這是我的第一個視窗")
    window.geometry("300x300")
    window.resizable(width=0, height=0)
    createTopLabel(window)
    createBottomLabel(window)
    window.mainloop()

def createTopLabel(root):
    font = tkFont.Font(family="Lucida Grande", size=20)
    label = tk.Label(root, text="這是我的第一個視窗", bg="#cccccc", font=font)
    label.pack(side="top",fill="x")

def createBottomLabel(root):
    font = tkFont.Font(family="Lucida Grande", size=25)
    label = tk.Label(root, text="這是下方的文字", bg="#cccccc", font=font)
    label.pack(side="bottom",fill="x")

if __name__ == "__main__":
    main()

