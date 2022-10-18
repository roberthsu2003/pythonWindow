import tkinter as tk

def createWindow():
    window = tk.Tk()
    window.title("這是我的第一個視窗")
    btn = tk.Button(window,text="請按我",padx=20,pady=20,font=('arial',16))
    btn.pack(padx=50,pady=30)
    window.mainloop()

def main():
    createWindow()

if __name__ == "__main__":
    main()