import tkinter as tk
from data import getStockInfo,readjson,load_user_option,save_user_option,subframe,line_opt_frame
from datetime import datetime
'''股票列表、股票資料，均會存成JSON檔，用於相關功能讀取'''

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("股價查詢系統")
        '''自動抓視窗位置'''
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        self.geometry(f'+{width // 2 - 600}+{height // 2 - 300}')
        '''自動抓視窗位置'''

        self.offline_mode = tk.BooleanVar()
        frameTOP = tk.Frame()
        frameTOP_l = tk.Frame(frameTOP)
        frameTOP_r = tk.Frame(frameTOP)

        frame1 = tk.Frame(frameTOP_l)
        frame2 = tk.Frame(frameTOP_l)

        frame2_l = tk.Frame(frame2)
        frame2_r = tk.Frame(frame2)
        frame2_1 = tk.Frame(frame2_l)
        frame2_2 = tk.Frame(frame2_r)

        self.frame3 = tk.Frame(frameTOP_l)
        frame3_4 = tk.Frame(frameTOP_l)
        self.frame4 = tk.Frame(frameTOP_l)
        self.frame5 = tk.Frame()
        self.frame67 = tk.Frame(frameTOP_r)
        self.frame6 = tk.Frame(self.frame67)
        self.frame7 = tk.Frame(self.frame67)


        tk.Label(frame1, text='新增股票代號', padx=10, pady=10).pack(side=tk.LEFT)
        self.add_stock_name=tk.StringVar()
        self.add_stock_name.set("2330")
        tk.Entry(frame1, textvariable=self.add_stock_name, width=10).pack(side=tk.LEFT)
        tk.Button(frame1, text='新增', padx=10, pady=1, command=self.addStock).pack(side=tk.LEFT)
        tk.Checkbutton(frame1, text='離線模式(顯示資料庫資料)', variable=self.offline_mode).pack(side=tk.LEFT)


        tk.Label(frame2_1, text='選擇股票',padx=10, pady=10).pack(side=tk.LEFT)
        scrollBar = tk.Scrollbar(frame2_1,orient="vertical")
        self.listboxselect_index = 0
        self.listBox = tk.Listbox(frame2_1,width=15,yscrollcommand=scrollBar.set)
        self.listBox.pack(side=tk.LEFT)
        self.listBox.bind("<<ListboxSelect>>",self.listBoxSelect)
        scrollBar.config(command=self.listBox.yview)
        scrollBar.pack(side=tk.LEFT)


        #tk.Button(frame2_2, text='LINE通知設定', padx=10, pady=1, command=self.line_option).grid(row=0, column=0)
        # 抱歉，此功能還沒寫好
        tk.Button(frame2_2, text='個股歷史查詢', padx=10, pady=1, command=self.open_subframe).grid(row=0, column=0)
        tk.Button(frame2_2, text='全部查詢', padx=10, pady=1, command=self.start_serchStockinfo).grid(row=1,column=0)
        tk.Button(frame2_2, text='停止更新', padx=10, pady=1, command=self.switch_off).grid(row=2,column=0)
        tk.Button(frame2_2, text='刪除此股票代號', padx=10, pady=1, command=self.delStock).grid(row=3,column=0)


        tk.Label(self.frame3, text='設定更新頻率(最低5秒):', padx=10, pady=10).pack(side=tk.LEFT)
        self.update_delay_text = tk.IntVar()
        self.update_delay_text.set(15)
        self.update_delay = self.update_delay_text.get()
        tk.Entry(self.frame3, textvariable=self.update_delay_text, width=10).pack(side=tk.LEFT)
        tk.Button(self.frame3, text='設定', padx=10, pady=1, command=self.set_update_delay).pack(side=tk.LEFT)

        tk.Label(frame3_4, text='現在時間:', padx=10, pady=10).pack(side=tk.LEFT)
        self.currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label = tk.Label(frame3_4, text=self.currentDateTime, padx=10, pady=10)
        self.time_label.pack(side=tk.LEFT)
        self.currenttime_run()


        tk.Label(self.frame4, text='資料下載時間:', padx=10, pady=10).pack(side=tk.LEFT)
        self.updatetime_label =tk.Label(self.frame4, text='尚未連線', padx=10, pady=10,fg="green")
        self.updatetime_label.pack(side=tk.LEFT)

        try:
            listbox_list = load_user_option()
            for item in listbox_list:
                self.listBox.insert(tk.END,item)
        except:
            pass

        frame1.pack(side=tk.TOP, fill=tk.X)

        frame2_1.pack(side=tk.TOP)
        frame2_2.pack(side=tk.TOP)
        frame2_l.pack(side=tk.LEFT)
        frame2_r.pack(side=tk.LEFT)
        frame2.pack(side=tk.TOP, fill=tk.X)

        self.frame3.pack(side=tk.TOP, fill=tk.X)
        frame3_4.pack(side=tk.TOP, fill=tk.X)
        self.frame4.pack(side=tk.TOP, fill=tk.X)

        frameTOP.pack(side=tk.TOP, fill=tk.X)
        self.frame5.pack(side=tk.TOP, fill=tk.X)
        frameTOP_l.pack(side=tk.LEFT, fill=tk.X)
        frameTOP_r.pack(side=tk.LEFT, fill=tk.X)

    def open_subframe(self):
        '''開啟歷史資料查詢視窗'''
        try:
            selected_name = self.selected_name
        except:
            self.updatetime_label.config(text="請先選擇一支股票", fg="red")
            return
        subframe(self,self.selected_name)


    def line_option(self):
        #抱歉，此功能還沒寫好
        line_opt_frame(self)

    def listBoxSelect(self,event):
        '''監聽選擇的股票list'''
        try:
            self.listboxselect_index = str(event.widget.curselection())[1]
            self.selected_name = self.listBox.get(self.listboxselect_index)

            global selectedname
            selectedname = self.selected_name[0:4]
            self.display_Info()
        except:
            return


    def currenttime_run(self):
        '''顯示現在時間功能'''
        self.currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text = self.currentDateTime)
        self.time_label.pack(side=tk.LEFT)

        self.after(1000, self.currenttime_run)

    def switch_off(self):
        '''停止自動更新'''
        self.updatetime_label.config(text="已停止更新",fg="red")
        try:
            self.after_cancel(self.serchstockinfo_timeloop)
        except:
            return

    def addStock(self):
        '''新增股票列表功能'''

        '''檢查股票代碼格式'''
        try:
            int(self.add_stock_name.get())
        except:
            return
        if len(self.add_stock_name.get()) != 4:
            return
        '''檢查股票代碼格式'''

        '''防止重複加入'''
        listbox_list = []
        for i in range(self.listBox.size()):
            listbox_list.append(self.listBox.get(i)[0:4])
        if self.add_stock_name.get() in listbox_list:
            return
        '''防止重複加入'''

        '''自動加入選擇的list上方，若失敗則加入到最後'''
        try:
            self.listBox.insert(self.listboxselect_index,self.add_stock_name.get())
        except:
            self.listBox.insert(tk.END, self.add_stock_name.get())
        '''自動加入選擇的list上方，若失敗則加入到最後'''

        '''將list存檔'''
        new_list=[]
        for i in range(self.listBox.size()):
            new_list.append(self.listBox.get(i))
        save_user_option(new_list)
        '''將list存檔'''

        self.listBox.pack(side=tk.LEFT)



    def delStock(self):
        self.listBox.delete(self.listboxselect_index)

        '''將list存檔'''
        new_list = []
        for i in range(self.listBox.size()):
            new_list.append(self.listBox.get(i))
        save_user_option(new_list)
        '''將list存檔'''

    def set_update_delay(self):
        if int(self.update_delay_text.get())<=5:
            self.update_delay_text.set(5)

        self.update_delay = self.update_delay_text.get()

        self.after_cancel(self.serchstockinfo_timeloop)
        self.start_serchStockinfo()

    def start_serchStockinfo(self):
        '''聯繫顯示即時資訊功能，先嘗試取消自動更新或啟動自動更新，再呼叫'''
        try:
            self.after_cancel(self.serchstockinfo_timeloop)
        except:
            pass
        self.serchStockinfo()

    def serchStockinfo(self):
        '''顯示即時資訊'''

        '''嘗試清空舊grid，不然再顯示容易有bug'''
        try:
            for item in self.grid_list:
                item.grid_forget()
        except:
            pass
        '''嘗試清空舊grid，不然再顯示容易有bug'''

        self.grid_list = []

        if self.offline_mode.get():
            self.updatetime_label.config(text="離線模式中",fg="red")
        else:
            self.updatetime_label.config(text=datetime.now().strftime("%H:%M:%S"),fg="green")


        for j in range(self.listBox.size()):
            try:
                self.stockinfo = getStockInfo(self.listBox.get(j)[0:4],self.offline_mode.get())
                if self.stockinfo is False:
                    self.updatetime_label.config(text="部分資料暫時無法連線或股票代碼錯誤", fg="red")
            except:
                if self.offline_mode.get():
                    self.updatetime_label.config(text="離線模式中: 缺少部分資料", fg="red")
                else:
                    self.updatetime_label.config(text="部分資料暫時無法連線或股票代碼錯誤",fg="red")
                continue

            item =[]
            for i in self.stockinfo:
                item.append(i)

            '''更新listbox股票名稱'''
            listbox_list = []
            try:
                for i in range(self.listBox.size()):
                    listbox_list.append(self.listBox.get(i))

                self.listBox.delete(listbox_list.index(self.stockinfo["股票名稱"][:4]))
                self.listBox.insert(self.listboxselect_index, self.stockinfo["股票名稱"])
            except:
                pass
            '''更新listbox股票名稱'''

            '''將list存檔'''
            new_list = []
            for i in range(self.listBox.size()):
                new_list.append(self.listBox.get(i))
            save_user_option(new_list)
            '''將list存檔'''



            for i in range(len(item)-1):
                if j == 0 and i ==len(item)-1:
                    pass
                elif j == 0:
                    tk.Label(self.frame5, text=item[i], padx=10, pady=10).grid(row=0+j*2, column=i)

                if i == 1:
                    self.grid_list.append(tk.Label(self.frame5, text=self.stockinfo[item[i]][5:], padx=10, pady=5))
                    self.grid_list[-1].grid(row=1 + j * 2, column=i)

                else:
                    self.grid_list.append(tk.Label(self.frame5, text=self.stockinfo[item[i]], padx=10, pady=5))
                    self.grid_list[-1].grid(row=1+j*2, column=i)

                '''漲跌顏色變化'''
                if i == 2:
                    if self.stockinfo[item[3]][0] == "-":
                        self.grid_list[-1].config(fg="green")
                    else:
                        self.grid_list[-1].config(fg="red")
                if i == 3:
                    if self.stockinfo[item[i]][0] == "-":
                        self.grid_list[-1].config(fg="green")
                    else:
                        self.grid_list[-1].config(fg="red")
                '''漲跌顏色變化'''


        try:
            self.display_Info()
        except:
            print("尚未選擇，因此無五檔顯示")
        self.updatetime_label.pack(side=tk.LEFT)

        self.serchstockinfo_timeloop = self.after(self.update_delay * 1000, self.serchStockinfo)

    def display_Info(self):
        '''顯示五檔報價'''
        file = readjson()
        best5 = file[selectedname]["五檔報價"]
        data_time = file[selectedname]["資料時間"]
        price = file[selectedname]["價格"]
        price2 = file[selectedname]["漲跌"]
        best5_name = file[selectedname]["股票名稱"][5:]
        best5_title = ["張數", "買價", "賣價", "張數"]
        try:
            self.display_label.config(text=f"{data_time}\n{best5_name}  {price}({price2[-6:]})")
        except:
            self.display_label = tk.Label(self.frame6, text=f"{data_time}\n{best5_name}  {price}({price2[-6:]})", padx=10, pady=10,font=('arial',12))
        self.display_label.pack(side=tk.TOP)

        for i in range(4):
            tk.Label(self.frame7, text=best5_title[i], padx=10, pady=10).grid(row=0, column=i + 2)

        for i in range(5):
            for j in range(4):
                control = tk.Label(self.frame7, text=best5[j + i * 4], padx=10, pady=10)
                control.grid(row=i + 1, column=j + 2)
                if j == 1:
                    control.config(fg="green")
                if j == 2:
                    control.config(fg="red")

        self.frame6.pack(side=tk.TOP)
        self.frame7.pack(side=tk.TOP)
        self.frame67.pack(side=tk.TOP, fill=tk.X)


if __name__ == "__main__":
    window = Window()
    window.mainloop()