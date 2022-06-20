from dataSource import getData
from dataSource import driver
import tkinter as tk
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.currentStockID = ""
        self.title("股票成交價及時查詢提醒系統")
        mainFrame  = tk.Frame(self, relief="groove", borderwidth=2)
        titleFrame = tk.Frame(mainFrame)
        tk.Label(titleFrame,text="股票成交價及時查詢提醒系統",font=("Arial",20,'bold'),fg="#555555").pack(padx=10)
        titleFrame.pack(pady=30)
        mainFrame.pack(pady=30,padx=30,ipadx=30,ipady=30)

        #-------------建立inputFrame-------------------
        self.inputFrame = tk.Frame(mainFrame,width=50)
        tk.Label(self.inputFrame, text="輸入欲查詢的股票號碼:",font=('Arial',13)).grid(row=0,column=0,sticky=tk.E)
        self.stockIDentry  = tk.Entry(self.inputFrame,text=tk.StringVar(),bd=5)
        self.stockIDentry.grid(row=0, column=1, sticky=tk.E)
        subminButton  = tk.Button(self.inputFrame, font=('Arial',15),text="搜尋",command=self.getStockID)
        subminButton.grid(row=0, column=2, sticky=tk.E)
        self.inputFrame.pack()

        #-----------建立顯示畫面-----------------------
        self.listFrame = tk.Frame(mainFrame)
        tk.Label(self.listFrame, text="公司名:", font=("Arial",14)).grid(row=0, column=0, sticky=tk.E, padx=10,pady=10)
        self.companyLabel = tk.Label(self.listFrame, text="", font=("Arial",14))
        self.companyLabel.grid(row=0,column=1,sticky=tk.W,padx=10,pady=10)
        self.listFrame.pack()

    def getStockID(self):
        inputID = self.stockIDentry.get()
        if inputID != self.currentStockID:
            self.currentStockID = inputID
            title, t_odd, odd, diff_odd, percent_diff = getData(self.currentStockID)
            self.companyLabel.configure(text=title)
            print(t_odd)
            print(odd)
            print(diff_odd)
            print(percent_diff)
        elif self.currentStockID == "":
            print("不可以為空字串")

def closeWindow():
    print("close window")
    window.destroy()
    driver.close()
    driver.quit()

if __name__ == "__main__":
    window = Window()
    window.resizable(width=0,height=0)
    window.protocol("WM_DELETE_WINDOW",closeWindow)

    window.mainloop()




