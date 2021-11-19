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
        mainFrame = tk.Frame(self,width=500,height=600,borderwidth=1,relief=tk.GROOVE)

        mainFrame.pack_propagate(0)
        mainFrame.pack(padx=50,pady=50)
        # --------------建立視窗end-------------------#



if __name__ == "__main__":
    window = Window()
    window.mainloop()