from datasource import getStackData
import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #name, allDataList = getStackData(2303)

        #建立mainFrame
        mainFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300)
        tk.Label(mainFrame,text="台股歷年經營績效查詢",font=("arial",20)).pack()

        mainFrame.pack(padx=20,pady=20)



if __name__ == "__main__":
    window = Window()
    window.title("台股歷年經營績效")
    window.mainloop()

