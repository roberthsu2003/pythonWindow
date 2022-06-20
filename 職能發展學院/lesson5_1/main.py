from dataSource import getData
from dataSource import driver
import tkinter as tk
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("股票成交價及時查詢提醒系統")

def closeWindow():
    print("close window")
    window.destroy()
    driver.close()
    driver.quit()

if __name__ == "__main__":
    window = Window()
    window.resizable(width=0,height=0)
    window.protocol("WM_DELETE_WINDOW",closeWindow)
    title, t_odd, odd, diff_odd, percent_diff = getData("2330")
    print(title)
    print(t_odd)
    print(odd)
    print(diff_odd)
    print(percent_diff)
    window.mainloop()




