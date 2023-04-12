import datasource
import tkinter as tk
from tkinter import ttk

sbi_numbers = 3
bemp_numbers = 3

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
#top_wrapperFrame=================
        top_wrapperFrame = ttk.Frame(self)
        top_wrapperFrame.pack(fill=tk.X)
#topFrame_start===================
        topFrame = ttk.LabelFrame(top_wrapperFrame,text="台北市行政區")
        length = len(datasource.sarea_list)
        self.radioStringVar = tk.StringVar()
        for i in range(length):
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame,text=datasource.sarea_list[i],value=datasource.sarea_list[i],variable=self.radioStringVar,command=self.radio_Event).grid(column=cols,row=rows,sticky=tk.W,padx=10,pady=10)

        topFrame.pack(side=tk.LEFT)
        self.radioStringVar.set('信義區')
        self.area_data = datasource.getInfoFromArea('信義區')
#topFrame_end===================

#sbi_warningFrame_start====================
        sbi_warningFrame = ttk.LabelFrame(top_wrapperFrame,text="可借目前不足站點")       
        
        sbi_warningFrame.pack(side=tk.LEFT)
#sbi_warningFrame_end======================

#bemp_warningFrame_start====================
        bemp_warningFrame = ttk.LabelFrame(top_wrapperFrame,text="可還目前不足站點")       
        
        bemp_warningFrame.pack(side=tk.LEFT)
#bemp_warningFrame_end======================

        bottomFrame = ttk.LabelFrame(self,text="信義區")
        bottomFrame.pack()

        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        self.tree = ttk.Treeview(bottomFrame, columns=columns, show='headings')
        self.tree.heading('#1', text='站點')
        self.tree.column("#1", minwidth=0, width=200)
        self.tree.heading('#2', text='時間')
        self.tree.column("#2", minwidth=0, width=200)
        self.tree.heading('#3', text='總車數')
        self.tree.column("#3", minwidth=0, width=50)
        self.tree.heading('#4', text='可借')
        self.tree.column("#4", minwidth=0, width=30)
        self.tree.heading('#5', text='可還')
        self.tree.column("#5", minwidth=0, width=30)
        self.tree.heading('#6', text='地址')
        self.tree.column("#6", minwidth=0, width=250)
        self.tree.heading('#7', text='狀態')
        self.tree.column("#7", minwidth=0, width=30)
        self.tree.pack(side=tk.LEFT)

        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['sna'][11:],item['mday'],item['tot'],item['sbi'],item['bemp'],item['ar'],item['act']])
        
#幫treeview加scrollbar------------------------------------------------

        scrollbar = ttk.Scrollbar(bottomFrame,command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

        #sorted by column in scrollbar

    '''
    self.tree.bind('<ButtonRelease-1>',self.sortby)

    def sortby(self,event):
        col = self.tree.identify_column(event.x)
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=True)
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sortby(col, 0))
    '''
        


        


    def radio_Event(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        area_name = self.radioStringVar.get()        
        self.area_data = datasource.getInfoFromArea(area_name)
        self.sbi_warning_data = datasource.filter_sbi_warning_data(self.area_data,sbi_numbers)
        print("sbi:")
        print(self.sbi_warning_data)
        self.bemp_waring_data = datasource.filter_bemp_warning_data(self.area_data,bemp_numbers)
        print("bemp:")
        print(self.bemp_waring_data)

        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['sna'][11:],item['mday'],item['tot'],item['sbi'],item['bemp'],item['ar'],item['act']])
        
        

def main():
    window = Window()
    window.title("台北市youbike2.0資訊")
    window.mainloop()

if __name__ == "__main__":
    main()