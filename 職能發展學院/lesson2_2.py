import tkinter

def main():
    window = tkinter.Tk()
    window.title("這是我的第一個視窗")
    window.geometry("300x300")
    window.resizable(width=0, height=0)
    window.mainloop()

if __name__ == "__main__":
    main()

