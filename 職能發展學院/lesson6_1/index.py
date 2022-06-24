import tkinter.ttk as ttk
import os
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("台積電,聯電,聯發科,鴻海歷史線圖")
        mainFrame  = tk.Frame(self, relief="groove", borderwidth=2)
        titleFrame = tk.Frame(mainFrame)
        tk.Label(titleFrame,text="台積電,聯電,聯發科,鴻海歷史線圖",font=("Arial",20,'bold'),fg="#555555").pack(padx=10)
        titleFrame.pack(pady=30)
        mainFrame.pack(pady=30,padx=30,ipadx=30,ipady=30)

        #-------------建立inputFrame-------------------
        self.inputFrame = tk.Frame(mainFrame,width=50)
        tk.Label(self.inputFrame, text="請選取股票號碼:",font=('Arial',13)).grid(row=0,column=0,sticky=tk.E)

        self.stock_choose = ttk.Combobox(self.inputFrame, width=27,state='readonly')
        self.stock_choose.bind('<<ComboboxSelected>>', self.combobox_selected)

        # Adding combobox drop down list

        self.stock_choose['values'] = ('台積電',
                                  '聯電',
                                  '聯發科',
                                  '鴻海',
                                  )

        self.stock_choose.grid(row=0, column=1, sticky=tk.E)
        self.inputFrame.pack()
        #-----------建立顯示畫面-----------------------

    def combobox_selected(self,event):
        column_names = ['2330.TW','2303.TW','2454.TW','2317.TW']
        index = self.stock_choose.current()
        column_name = column_names[index]
        image_name = column_name+'.png'
        abs_file_name = os.path.abspath('./assets/2022-06-25.csv')
        dataFrame = pd.read_csv(abs_file_name)
        dataFrame['Date'] = pd.to_datetime(dataFrame['Date'])
        dataFrame['2330.TW'] = dataFrame['2330.TW'].round(2)
        dataFrame['2303.TW'] = dataFrame['2303.TW'].round(2)
        dataFrame['2454.TW'] = dataFrame['2454.TW'].round(2)
        dataFrame['2317.TW'] = dataFrame['2317.TW'].round(2)
        figure = plt.figure(figsize=(10, 5))
        ax1 = figure.add_subplot(1, 1, 1)
        ax1.plot(dataFrame['Date'], dataFrame[column_name])
        plt.title(column_name)
        plt.savefig("./assets/" + image_name)








def closeWindow():
    print("close window")
    window.destroy()



if __name__ == "__main__":
    window = Window()
    window.resizable(width=0,height=0)
    window.protocol("WM_DELETE_WINDOW",closeWindow)
    window.mainloop()




