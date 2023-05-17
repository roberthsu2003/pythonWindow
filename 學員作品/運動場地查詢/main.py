import datetime
from tkinter.simpledialog import askstring
import datasource
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

#建立menu=========================
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.command_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='查詢', menu=self.command_menu)
        self.command_menu.add_command(
            label='用途查詢', command=self.show_combobox)
        self.command_menu.add_separator()
        self.command_menu.add_command(
            label='地址查詢', command=self.menu_address_search_click)
#===============================

#建立main frame=================
        mainFrame = ttk.Frame(self)
        mainFrame.pack(padx=10,pady=10)
#===============================

#建立logo========================
        logoImage = Image.open('picture/pic1.jpg')
        resizeImage = logoImage.resize((700, 190), Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(mainFrame, image=self.logoTkimage)
        logoLabel.pack(pady=(0, 20))
#================================

#建立top_wrapperFrame=============
        top_wrapperFrame = ttk.Frame(mainFrame)
        top_wrapperFrame.pack(fill=tk.X)
#=================================

#建立radiobutton的labelframe=======
        topFrame = ttk.LabelFrame(top_wrapperFrame,text='台北市行政區')
        length = len(datasource.area_list)
        self.radioStringVar = tk.StringVar()
        for i in range(length):
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame, text=datasource.area_list[i], value=datasource.area_list[i], variable=self.radioStringVar,command=self.radio_Event).grid(
                column=cols, row=rows, sticky=tk.W, padx=20, pady=10)
        topFrame.pack(side=tk.LEFT)
        self.radioStringVar.set('中山區')
        self.area_data = datasource.getInfoFromArea('中山區')
#==================================

#建立查詢結果treeview的labelframe============
        self.searchFrame = ttk.LabelFrame(top_wrapperFrame,text='查詢結果')
        self.searchFrame.pack()
        columns = ('#1','#2','#3','#4','#5')
        self.serch_tree = ttk.Treeview(
            self.searchFrame, columns=columns, show='headings')
        self.serch_tree.heading('#1',text='場地名稱')
        self.serch_tree.column('#1',minwidth=0,width=150)
        self.serch_tree.heading('#2',text='用途')
        self.serch_tree.column('#2',minwidth=0,width=65)
        self.serch_tree.heading('#3',text='地址')
        self.serch_tree.column('#3',minwidth=0,width=300)
        self.serch_tree.heading('#4',text='開放時間')
        self.serch_tree.column('#4',minwidth=0,width=100)
        self.serch_tree.heading('#5',text='結束時間')
        self.serch_tree.column('#5',minwidth=0,width=100)
        self.serch_tree.pack(side=tk.LEFT)

        #建立serch_tree的scrollbar
        serch_scrollbar = ttk.Scrollbar(self.searchFrame, command=self.serch_tree.yview)
        serch_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.serch_tree.config(yscrollcommand=serch_scrollbar.set)
#=========================================

#建立bottomframe===========================
        now = datetime.datetime.now()
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")
        self.bottomFrame = ttk.LabelFrame(mainFrame, text=f"中山區-{nowString}")
        self.bottomFrame.pack()
        
        #建立treeview
        columns = ('#1','#2','#3','#4','#5')
        self.tree = ttk.Treeview(self.bottomFrame, columns=columns,show='headings')
        self.tree.heading('#1',text='場地名稱')
        self.tree.column('#1',minwidth=0,width=150)
        self.tree.heading('#2',text='用途')
        self.tree.column('#2',minwidth=0,width=65)
        self.tree.heading('#3',text='地址')
        self.tree.column('#3',minwidth=0,width=300)
        self.tree.heading('#4',text='開放時間')
        self.tree.column('#4',minwidth=0,width=100)
        self.tree.heading('#5',text='結束時間')
        self.tree.column('#5',minwidth=0,width=100)
        self.tree.pack(side=tk.LEFT)

        #列出area_data並放入treeview
        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])

        #建立treeview的scrollbar
        scrollbar = ttk.Scrollbar(self.bottomFrame,command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
#=============================================

#製作combobox=================================
    def show_combobox(self):
        self.type_data = datasource.type_list
        combobox_win = tk.Toplevel(self)
        combobox_win.geometry("220x100")
        combobox_win.title('用途查詢')

        #抓取點選的值
        def combobox_callback(event):
            selected_value = combobox.get()
            self.menu_use_search_click(selected_value)

        #放入combobox選項
        values = self.type_data
        combobox = ttk.Combobox(combobox_win, values=values, state='readonly')
        combobox.pack(pady=10)
        combobox.current(0)
        #綁定combobox_callback事件
        combobox.bind('<<ComboboxSelected>>', combobox_callback)
#============================================

#建立點選radiobutton的事件====================
    def radio_Event(self):

        now = datetime.datetime.now()
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")
        area_name = self.radioStringVar.get()
        self.bottomFrame.config(text=f"{area_name}-{nowString}")

        for item in self.tree.get_children():
            self.tree.delete(item)

        area_name = self.radioStringVar.get()
        self.area_data = datasource.getInfoFromArea(area_name)
        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])
#=============================================

#建立點選用途查詢(combobox)的事件================
    def menu_use_search_click(self,selected_value):
        for item in self.serch_tree.get_children():
            self.serch_tree.delete(item)
        for item in self.area_data:
            if selected_value in item['SportType'] or selected_value in item['Name']:
                self.serch_tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])
#=============================================

#建立輸入地址查詢的事件========================
    def menu_address_search_click(self):
        try:
            retVal = askstring('地址搜尋', '請輸入地址')
            for item in self.serch_tree.get_children():
                self.serch_tree.delete(item)
            for item in self.area_data:
                if retVal in item['Address']:
                    self.serch_tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])
        except TypeError:
            pass
#=============================================

def main():
    window = Window()
    window.title('台北市運動場地')
    window.mainloop()

if __name__ == '__main__':
    main()