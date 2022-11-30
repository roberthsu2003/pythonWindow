import datasource as ds
from secrets import api_key
import tkinter as tk

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
        city_forcast=ds.get_forcast_data(ename,api_key)
        print(cname)
        print(city_forcast)

            


        

        


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
