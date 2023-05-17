import datasource
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter.simpledialog import askstring
from PIL import Image,ImageTk


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #===========================SearchMenu========================================
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.command_menu = tk.Menu(self.menubar)
        self.command_menu.add_command(label="搜尋", command=self.Menu_Search)
        self.menubar.add_cascade(label="地名關鍵字搜尋", menu=self.command_menu)
        #===========================SearchMenu========================================
        #===========================MainFrame========================================
        MainFrame = ttk.Frame(self)
        MainFrame.pack(padx=50,pady=50)
        #===========================LogoImage========================================
        logoImage = Image.open('logo.png')
        resizeImage = logoImage.resize((400,100),Image.LANCZOS)
        self.logoTKImage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(MainFrame,image=self.logoTKImage,width=400)
        logoLabel.pack(pady=30)
        #===========================LogoImage========================================
        #===========================MainFrame========================================
        #===========================TopFrame========================================
        TopFrame = ttk.LabelFrame(MainFrame,text='桃園機場各航空公司')
        Length = len(datasource.airportname_list)
        self.radioStrVar= tk.StringVar()
        for i in range(Length):
            cols = i % 10
            rows = i // 10
            ttk.Radiobutton(TopFrame,text=datasource.airportname_list[i],value=datasource.airportname_list[i],variable=self.radioStrVar,command=self.Radio_Event).grid(column=cols,row=rows,sticky=tk.W,padx=10,pady=10)
        TopFrame.pack()
        self.radioStrVar.set('星宇航空')
        self.airport_data = datasource.getInfoFromAirPort('星宇航空')
        #===========================TopFrame========================================

        #===========================CenterFrame========================================
        CenterFrame = ttk.LabelFrame(MainFrame,text='查詢結果欄位')
        CenterFrame.pack()
        columns = ('#1', '#2', '#3', '#4','#5','#6','#7','#8','#9')
        self.treeC = ttk.Treeview(CenterFrame, columns=columns, show='headings')
        self.treeC.heading('#1', text='航廈')
        self.treeC.column('#1',minwidth=0,width=50)
        self.treeC.heading('#2', text='航空公司代碼')
        self.treeC.column('#2',minwidth=0,width=100)
        self.treeC.heading('#3', text='航空公司中文')
        self.treeC.column('#3',minwidth=0,width=100)
        self.treeC.heading('#4', text='班次')
        self.treeC.column('#4',minwidth=0,width=100)
        self.treeC.heading('#5', text='登機門/機坪')
        self.treeC.column('#5',minwidth=0,width=100)
        self.treeC.heading('#6', text='預計日期')
        self.treeC.column('#6',minwidth=0,width=100)
        self.treeC.heading('#7', text='預計時間')
        self.treeC.column('#7',minwidth=0,width=100)
        self.treeC.heading('#8', text='往來地點中文')
        self.treeC.column('#8',minwidth=0,width=100)
        self.treeC.heading('#9', text='航班狀態')
        self.treeC.column('#9',minwidth=0,width=100)
        self.treeC.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(CenterFrame,command=self.treeC.yview)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.treeC.config(yscrollcommand=scrollbar.set)
        #===========================CenterFrame========================================

        #===========================BottomFrame=====================================
        now = datetime.datetime.now()
        nowString = now.strftime('%Y-%m-%d %H:%M:%S')
        self.BottomFrame = ttk.LabelFrame(MainFrame,text=f'星宇航空--{nowString}')
        self.BottomFrame.pack()

        columns = ('#1', '#2', '#3', '#4','#5','#6','#7','#8','#9','#10')
        self.tree = ttk.Treeview(self.BottomFrame, columns=columns, show='headings')
        self.tree.heading('#1', text='航廈')
        self.tree.column('#1',minwidth=0,width=50)
        self.tree.heading('#2', text='班次')
        self.tree.column('#2',minwidth=0,width=100)
        self.tree.heading('#3', text='登機門/機坪')
        self.tree.column('#3',minwidth=0,width=100)
        self.tree.heading('#4', text='表訂日期')
        self.tree.column('#4',minwidth=0,width=100)
        self.tree.heading('#5', text='表訂時間')
        self.tree.column('#5',minwidth=0,width=100)
        self.tree.heading('#6', text='預計日期')
        self.tree.column('#6',minwidth=0,width=100)
        self.tree.heading('#7', text='預計時間')
        self.tree.column('#7',minwidth=0,width=100)
        self.tree.heading('#8', text='往來地點')
        self.tree.column('#8',minwidth=0,width=100)
        self.tree.heading('#9', text='航班狀態')
        self.tree.column('#9',minwidth=0,width=100)
        self.tree.heading('#10', text='機型')
        self.tree.column('#10',minwidth=0,width=100)
        self.tree.pack(side=tk.LEFT)

        for item in self.airport_data:
            self.tree.insert('',tk.END,values=[item['航廈'],item['班次'],item['登機門/機坪'],item['表訂日期'],item['表訂時間'],item['預計日期'],item['預計時間'],item['往來地點中文'],item['航班狀態'],item['機型']])

        scrollbar = ttk.Scrollbar(self.BottomFrame,command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
    #===========================BottomFrame=====================================
    #===========================Menu_Search=====================================
    def Menu_Search(self):
        enter = askstring("搜尋目的地","請輸入地名關鍵字")
        for child in self.treeC.get_children():
            self.treeC.delete(child)
        for item in datasource.data_list:
            if enter in item['往來地點中文']:
                self.treeC.insert('',tk.END,values=[item['航廈'],item['航空公司代碼'],item['航空公司中文'],item['班次'],item['登機門/機坪'],item['預計日期'],item['預計時間'],item['往來地點中文'],item['航班狀態']])
    #===========================Menu_Search=====================================
    #===========================Radio_Event=====================================
    def Radio_Event(self):
        now = datetime.datetime.now()
        nowString = now.strftime('%Y-%m-%d %H:%M:%S')
        for item in self.tree.get_children():
            self.tree.delete(item)
        airport_name = self.radioStrVar.get()
        self.BottomFrame.config(text=f'{airport_name}--{nowString}')
        self.airport_data = datasource.getInfoFromAirPort(airport_name)
        for item in self.airport_data:
            self.tree.insert('',tk.END,values=[item['航廈'],item['班次'],item['登機門/機坪'],item['表訂日期'],item['表訂時間'],item['預計日期'],item['預計時間'],item['往來地點中文'],item['航班狀態'],item['機型']])
    #===========================Radio_Event=====================================
def main():
    windows = Window()
    windows.title('桃園機場查詢系統')
    windows.mainloop()

if __name__=='__main__':
    main()