import datasource
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = ttk.LabelFrame(self,text="台北市行政區")
        length = len(datasource.sarea_list)
        self.radioStringVar = tk.StringVar()
        for i in range(length):
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame,text=datasource.sarea_list[i],value=datasource.sarea_list[i],variable=self.radioStringVar,command=self.radio_Event).grid(column=cols,row=rows,sticky=tk.W,padx=10,pady=10)

        topFrame.pack()
        self.radioStringVar.set('信義區')
        self.area_data = datasource.getInfoFromArea('信義區')

        bottomFrame = ttk.LabelFrame(self,text="信義區")
        bottomFrame.pack()

        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        tree = ttk.Treeview(bottomFrame, columns=columns, show='headings')
        tree.heading('#1', text='站點')
        tree.column("#1", minwidth=0, width=200)
        tree.heading('#2', text='時間')
        tree.column("#2", minwidth=0, width=200)
        tree.heading('#3', text='總車數')
        tree.column("#3", minwidth=0, width=50)
        tree.heading('#4', text='可借')
        tree.column("#4", minwidth=0, width=30)
        tree.heading('#5', text='可還')
        tree.column("#5", minwidth=0, width=30)
        tree.heading('#6', text='地址')
        tree.column("#6", minwidth=0, width=250)
        tree.heading('#7', text='狀態')
        tree.column("#7", minwidth=0, width=30)
        tree.pack()

        for item in self.area_data:
            tree.insert('',tk.END,values=[item['sna'][11:],item['mday'],item['tot'],item['sbi'],item['bemp'],item['ar'],item['act']])


    def radio_Event(self):
        area_name = self.radioStringVar.get()
        self.area_data = datasource.getInfoFromArea(area_name)
        for item in self.area_data:
            print(item)

def main():
    window = Window()
    window.title("台北市youbike2.0資訊")
    window.mainloop()

if __name__ == "__main__":
    main()