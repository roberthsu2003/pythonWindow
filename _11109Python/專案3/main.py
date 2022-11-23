import datasource as ds
from secrets import api_key
import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        tk.Label(self,text="各縣市4天天氣預測",font=('Arial', 20)).pack(padx=30,pady=30)

        #建立存放按鈕的容器
        buttons_frame = tk.Frame(self,background="#333333",width=200,height=300)
        buttons_frame.pack()
        

        


def main():
    window = Window()
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
