import tkinter as tk
import dataSource
from tkinter import messagebox

class Window(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("全省空氣品質指標")

        #--------------取得資料start-------------------#
        try:
            self.cities = dataSource.getAirData()
        except ValueError as e:
            messagebox.showwarning("連線錯誤",e)
            self.destroy()

        for city in self.cities: #self.cities是list,內容元素是CityWeather的實體
            print(city.county)
        # --------------取得資料end-------------------#

        # --------------建立視窗start-------------------#
        mainFrame = tk.Frame(self,width=500,height=600,borderwidth=1,relief=tk.GROOVE,padx=20,pady=20)

        #建立上方的topFrame
        topFrame = tk.Frame(mainFrame)
        tk.Label(topFrame,text="台灣各地空氣品質指標",font=("arial",22,"bold"),fg="#555555").pack()
        self.currentTimeLabel = tk.Label(topFrame,text="觀測時間:xxxxxxxxx",font=("arial",16),fg="#555555")
        self.currentTimeLabel.pack(pady=(30,10))
        self.nextTimeLabel = tk.Label(topFrame,text="下次更新:xxxxxxxxx",font=("arial",16),fg="#555555")
        self.nextTimeLabel.pack()
        self.leftTimeLabel = tk.Label(topFrame, text="20:15", font=("arial", 16), fg="#555555")
        self.leftTimeLabel.pack()
        topFrame.pack()
        mainFrame.pack_propagate(0)
        mainFrame.pack(padx=50,pady=50)
        # --------------建立視窗end-------------------#



if __name__ == "__main__":
    window = Window()
    window.mainloop()