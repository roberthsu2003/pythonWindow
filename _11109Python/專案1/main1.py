import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        mainFrame = tk.Frame(self,bg='#345678',width=800,height=500)
        
        mainFrame.pack()


def main():
    window = Window()
    window.title("Frame框架")
    window.geometry("800x500")
    window.mainloop()

if __name__ == "__main__":
    main()