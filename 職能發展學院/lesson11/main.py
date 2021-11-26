import tkinter as tk
import dataSource
from tkinter import messagebox
import tkinter.ttk as ttk
from datetime import datetime

class Window(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("全省空氣品質指標")

        #--------------取得資料start-------------------#
        try:
            citylist = dataSource.getAirData()
            self.cities = {cityObject.county:cityObject for cityObject in citylist} #包存現在要顯示的資料,轉成dict,key=城市名,value=CityWeather的實體
        except ValueError as e:
            messagebox.showwarning("連線錯誤",e)
            self.destroy()

        currentTimeString = citylist[0].time #取得json內顯示的時間字串
        self.currentDateTime = datetime.strptime(currentTimeString,"%Y-%m-%d %H:%M:%S.%f") #將字串轉為datetime物件,保存目前顯示資料的datetime物件

        print(self.currentDateTime)
        print(self.cities)


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

        #建立中間的middleFrame
        middleFrame = tk.Frame(mainFrame)
        tk.Label(middleFrame,text="請選擇監測站:",font=("arial",16),fg="#555555").pack(side=tk.LEFT)
        comboBox = ttk.Combobox(middleFrame, values=['apple','banana','orange','lemon','tomato'])
        comboBox.pack(side=tk.LEFT)
        comboBox.current(0)
        comboBox.bind('<<ComboboxSelected>>', self.combobox_selected)
        middleFrame.pack(pady=20)


        mainFrame.pack_propagate(0)
        mainFrame.pack(padx=50,pady=50)
        # --------------建立視窗end-------------------#

    def combobox_selected(self,event):
        widget = event.widget
        comboBoxIndex = widget.current()
        print(comboBoxIndex)

if __name__ == "__main__":
    window = Window()
    window.mainloop()