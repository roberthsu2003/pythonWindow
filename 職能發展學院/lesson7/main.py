from datasource import getStackData
import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #name, allDataList = getStackData(2303)

        #建立mainFrame
        mainFrame = tk.Frame(self,relief=tk.GROOVE,borderwidth=1,width=300,height=200)
        tk.Label(mainFrame,text="台股歷年經營績效查詢",font=("arial",20),bg="#333333",fg='#ffffff',padx=10,pady=10).pack(pady=20)
        inputFrame = tk.Frame(mainFrame)
        tk.Label(inputFrame, text="股票編號:", font=("arial", 20)).pack(side=tk.LEFT)
        tk.Entry(inputFrame,font=("arial", 16),width=7).pack(side=tk.LEFT)
        inputFrame.pack()

        tk.Button(mainFrame,text="確定",padx=40,pady=20).pack(pady=20)
        mainFrame.pack_propagate(0) #取消frame以子項的內容為預設的大小
        mainFrame.pack(padx=20,pady=20)



if __name__ == "__main__":
    window = Window()
    window.title("台股歷年經營績效")
    window.mainloop()

