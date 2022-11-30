import datasource as ds
from secrets import api_key
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,cities_dict):
        super().__init__()
        tk.Label(self,text="各縣市4天天氣預測",font=('Arial', 20)).pack(padx=30,pady=30)

        #建立存放按鈕的容器
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(padx=50,pady=(0,30))
        #設定grid的row數量
        grid_row_nums = 3
        for index,cities in enumerate(cities_dict.items()):
            cname, ename = cities
            btn = tk.Button(buttons_frame,text=f"{cname}\n{ename}",font=('arial',15),width=8,padx=20,pady=5)
            btn.grid(row=index % grid_row_nums,column=index // grid_row_nums)
            btn.bind("<Button>",self.button_click)

        
        


    
    #實體的方法
    def button_click(self,event):
        btn_text = event.widget['text']
        name_list = btn_text.split("\n")
        cname = name_list[0]
        ename = name_list[1]        
        city_forcase=ds.get_forcast_data(ename,api_key)        
        if hasattr(self,'displayFrame'):
            self.displayFrame.destroy()
        self.displayFrame = DisplayFrame(self,data=city_forcase,text=cname,borderwidth=2,relief=tk.GROOVE)
        self.displayFrame.pack(padx=50,pady=(0,30))



class DisplayFrame(ttk.LabelFrame):
    def __init__(self,parent,data=None,**kwargs):        
        super().__init__(parent,**kwargs)
        self.city_data = data
        
        #資料拆成3份
        total_rows = len(self.city_data)
        column_rows = total_rows // 3 + 1
        leftData = self.city_data[:column_rows]
        centerData = self.city_data[column_rows:column_rows*2]
        rightData = self.city_data[column_rows*2:]


        leftFrame = CustomFrame(self,data=leftData)
        leftFrame.pack(side=tk.LEFT)

        centerFrame = CustomFrame(self,data=centerData)
        centerFrame.pack(side=tk.LEFT)

        rightFrame = CustomFrame(self,data=rightData)
        rightFrame.pack(side=tk.LEFT)

class CustomFrame(tk.Frame):
    def __init__(self,parent,data=None,**kwarge):
        super().__init__(parent,**kwarge)
        self.list_data = data
        print(self.list_data)
        self.tree = ttk.Treeview(self,columns=['#1','#2','#3','#4'])
        self.tree.pack(side=tk.LEFT)

        self.tree.heading('#1',text="時間")
        self.tree.heading('#2',text="溫度")
        self.tree.heading('#3',text="狀態")
        self.tree.heading('#4',text="溼度")

        self.tree.column('#1',width=120,anchor='center')
        self.tree.column('#2',width=50,anchor='center')
        self.tree.column('#3',width=80,anchor='center')
        self.tree.column('#4',width=50,anchor='center')

        for item in self.list_data:
            self.tree.insert('',tk.END,values=item)
        



        

        


def main():
    window = Window(ds.tw_county_names)
    window.title("各縣市4天天氣預測")
    window.mainloop()

    '''
    try:
        list_data = ds.get_forcast_data(ds.tw_county_names["金門"],api_key)
    except Exception as e:
        print(e)
        return
    
    for item in list_data:
        print(item['dt_txt'])
    '''
    

if __name__ == "__main__":
    main()
