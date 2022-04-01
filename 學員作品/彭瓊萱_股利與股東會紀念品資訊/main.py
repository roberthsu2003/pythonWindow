import tkinter as tk
from tkinter import ttk
from tkinter import font
import dataSource.dataSource_StockDividendPolicy as dsStockDividend
import dataSource.dataSource_Meeting as dsMeeting
from tkinter import messagebox
from datetime import datetime
import time

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        # 標題的Frame ===== start
        topFrame = tk.Frame(self, bg='red')
        tk.Label(topFrame, text="股利與股東會紀念品資訊", font=("arial", 20, "bold"), bg='yellow').pack()
        # topFrame.grid(column=0, row=0, columnspan=2, padx=20, pady=20)
        topFrame.grid(column=0, row=0, columnspan=2)
        # 標題的Frame ===== end

        # 左方容器Frame ===== start
        self.LeftLabelFrame = LeftLabelFrame(self, text="股利資訊")
        self.LeftLabelFrame.grid(column=0, row=1, padx=20, pady=20)
        # self.LeftLabelFrame.grid(column=0, row=1)
        # 左方容器Frame ===== end

        # 右方容器Frame ===== start
        self.RightLabelFrame = RightLabelFrame(self, text="股東會紀念品資訊")
        # self.RightLabelFrame.grid(column=0, row=2, padx=20, pady=20)
        self.RightLabelFrame.grid(column=0, row=2)
        # 右方容器Frame ===== end

        # 下方容器Frame ===== start
        footerFrame = tk.Frame(self)
        closeButton = tk.Button(footerFrame, text="關閉", command=exit, font=("arial", 14))
        closeButton.pack(side=tk.BOTTOM, ipadx=5, ipady=5)
        # footerFrame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        footerFrame.grid(row=3, column=0, padx=10, pady=10)
        # 下方容器Frame ===== start

class LeftLabelFrame(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        left_top_frame = tk.Frame(self)

        id_Font = font.Font(family='Helvetica', size=14)
        idLabel = ttk.Label(left_top_frame, font=id_Font, text="股票代碼:")
        # idLabel.pack(side=tk.LEFT, padx=(50, 0), ipady=10)
        idLabel.pack(side=tk.LEFT, padx=(50, 0), ipady=10)

        self.varId = tk.StringVar()
        id_text = tk.Entry(left_top_frame, show=None, textvariable=self.varId)
        id_text.pack(side=tk.LEFT, padx=10)

        def queryClick():
            print("queryClick...")

            # 清除tree內容
            for i in self.tree.get_children():
                self.tree.delete(i)

            stockId = id_text.get()
            if stockId == "":
                messagebox.showinfo("訊息視窗", "請先輸入股票代碼！")
                return
            records = dsStockDividend.get_stock_info(stockId)
            if (records == None) or (len(records) == 0):
                dsStockDividend.download_save_to_DataBase(stockId)
                time.sleep(0.3)
                records = dsStockDividend.get_stock_info(stockId)

            if records == None:
                messagebox.showinfo("訊息視窗", "查無資料")
            else:
                # for record in records:
                    # self.tree.insert('', tk.END, values=record)

                i = 1
                for item in records:
                    newItem = (i,) + item
                    # treeView.insert('', 'end', values=item)
                    if i % 2 == 0:
                        self.tree.insert('', 'end', values=newItem, tags='evenrow')
                    else:
                        self.tree.insert('', 'end', values=newItem, tags='oddrow')
                    i += 1

                dividend = dsStockDividend.get_dividend(stockId)
                if dividend != None:
                    cheap = float(dividend) * 15
                    fairprice = float(dividend) * 20
                    expensive = float(dividend) * 30
                    msgText = '便宜價是{0:.2f}, 合理價是{1:.2f}, 昂貴價是{2:.2f}'.format(cheap, fairprice, expensive)
                    self.priceLabel["text"] = msgText

        button_Font = font.Font(family='Helvetica', size=14)
        queryButton = tk.Button(left_top_frame, font=button_Font, text="查詢", command=queryClick)
        queryButton.pack(side=tk.LEFT, padx=10)

        price_Font = font.Font(family='Helvetica', size=14)
        self.priceLabel = ttk.Label(self, font=price_Font)
        self.priceLabel.pack(side=tk.BOTTOM, padx=(50, 0))
        left_top_frame.pack()

        bottom_frame = tk.Frame(self)
        scrollbar1 = tk.Scrollbar(bottom_frame)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        # self.tree = ttk.Treeview(bottom_frame, columns=('no', 'id', 'name', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9'), show='headings', yscrollcommand=scrollbar1.set)
        self.tree = ttk.Treeview(bottom_frame,
                                 columns=('no', 'id', 'name', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9'),
                                 show='headings', yscrollcommand=scrollbar1.set, height=8)
        self.tree.heading('no', text='編號')
        self.tree.heading('id', text='股票代碼')
        self.tree.heading('name', text='名稱')
        self.tree.heading('f1', text='股利年度')
        self.tree.heading('f2', text='現金股利')
        self.tree.heading('f3', text='股票股利')
        self.tree.heading('f4', text='合計')
        self.tree.heading('f5', text='填息花費日數')
        self.tree.heading('f6', text='最高股價')
        self.tree.heading('f7', text='最高股價')
        self.tree.heading('f8', text='年均股價')
        self.tree.heading('f9', text='年均殖利率(%)')
        self.tree.column('no', width=40)
        self.tree.column('id', width=100)
        self.tree.column('name', width=100)
        self.tree.column('f1', width=100)
        self.tree.column('f2', width=100)
        self.tree.column('f3', width=100)
        self.tree.column('f4', width=100)
        self.tree.column('f5', width=100)
        self.tree.column('f6', width=100)
        self.tree.column('f7', width=100)
        self.tree.column('f8', width=100)
        self.tree.column('f9', width=100)
        self.tree.pack(side=tk.TOP)
        scrollbar1.config(command=self.tree.yview)
        self.tree.tag_configure("oddrow", background='#ff9', foreground='black')
        self.tree.tag_configure("evenrow", background='lightblue', foreground='black')
        bottom_frame.pack()


class RightLabelFrame(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        left_top_frame = tk.Frame(self)

        id_Font = font.Font(family='Helvetica', size=14)
        idLabel = ttk.Label(left_top_frame, font=id_Font, text="股票代碼:")
        idLabel.pack(side=tk.LEFT, padx=(50, 0), ipady=10)

        self.varId = tk.StringVar()
        id_text = tk.Entry(left_top_frame, show=None, textvariable=self.varId)
        id_text.pack(side=tk.LEFT, padx=10)

        def queryClick():
            print("queryClick...")

            # 清除tree內容
            for i in self.tree.get_children():
                self.tree.delete(i)

            stockId = id_text.get()
            if stockId == "":
                messagebox.showinfo("訊息視窗", "請先輸入股票代碼！")
                return
            records = dsMeeting.get_meeting_info(stockId)
            if (records == None) or (len(records) == 0):
                time.sleep(0.3)
                records = dsMeeting.get_meeting_info(stockId)

            if records == None or len(records) == 0:
                messagebox.showinfo("訊息視窗", "查無資料")
            else:
                for record in records:
                    self.tree.insert('', tk.END, values=record)

        button_Font = font.Font(family='Helvetica', size=14)
        queryButton = tk.Button(left_top_frame, font=button_Font, text="查詢", command=queryClick)
        queryButton.pack(side=tk.LEFT, padx=10)

        # def queryYearClick():
        #     print("queryYearClick...")
        #
        #     # 清除tree內容
        #     for i in self.tree.get_children():
        #         self.tree.delete(i)
        #
        #     records = dsMeeting.get_meetings_of_oneyear_info()
        #     if records == None:
        #         messagebox.showinfo("訊息視窗", "查無資料")
        #     else:
        #         # for record in records:
        #         #     self.tree.insert('', tk.END, values=record)
        #
        #         i = 1
        #         for item in records:
        #             newItem = (i,) + item
        #             # treeView.insert('', 'end', values=item)
        #             if i % 2 == 0:
        #                 self.tree.insert('', 'end', values=newItem, tags='evenrow')
        #             else:
        #                 self.tree.insert('', 'end', values=newItem, tags='oddrow')
        #             i += 1

        def queryMettingInfo(m_year = '2022', m_type=0):

            # 清除tree內容
            for i in self.tree.get_children():
                self.tree.delete(i)

            records = dsMeeting.get_meetings_of_oneyear_info(m_year, m_type)
            if records == None:
                messagebox.showinfo("訊息視窗", "查無資料")
            else:
                # for record in records:
                #     self.tree.insert('', tk.END, values=record)

                i = 1
                for item in records:
                    newItem = (i,) + item
                    # treeView.insert('', 'end', values=item)
                    if i % 2 == 0:
                        self.tree.insert('', 'end', values=newItem, tags='evenrow')
                    else:
                        self.tree.insert('', 'end', values=newItem, tags='oddrow')
                    i += 1

        def getThisYear():
            tempdate = datetime.today()
            thisYear = tempdate.strftime('%Y')
            return thisYear

        def queryYearClick():
            print("queryYearClick...")
            thisYear = getThisYear()
            queryMettingInfo(thisYear, 0)

        def queryYearNotExpiredClick():
            print("queryYearNotExpiredClick...")
            thisYear = getThisYear()
            queryMettingInfo(thisYear, 1)

        def queryYearExpiredClick():
            print("queryYearExpiredClick...")
            thisYear = getThisYear()
            queryMettingInfo(thisYear, 2)

        button_Font = font.Font(family='Helvetica', size=14)
        queryButton = tk.Button(left_top_frame, font=button_Font, text="查詢當年度資料", command=queryYearClick)
        queryButton.pack(side=tk.LEFT, padx=10)

        queryNotExpiredButton = tk.Button(left_top_frame, font=button_Font, text="查詢當年度未到期資料", command=queryYearNotExpiredClick)
        queryNotExpiredButton.pack(side=tk.LEFT, padx=10)

        queryExpiredButton = tk.Button(left_top_frame, font=button_Font, text="查詢當年度已到期資料", command=queryYearExpiredClick)
        queryExpiredButton.pack(side=tk.LEFT, padx=10)

        left_top_frame.pack()

        bottom_frame = tk.Frame(self)
        self.tree = ttk.Treeview(bottom_frame, columns=('no', 'YER', 'id', 'name', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10'), show='headings', height=5)
        self.tree.heading('no', text='編號')
        self.tree.heading('YER', text='開會年度')
        self.tree.heading('id', text='代碼')
        self.tree.heading('name', text='名稱')
        self.tree.heading('f1', text='股價')
        self.tree.heading('f2', text='最後買進日')
        self.tree.heading('f3', text='股東會日期')
        self.tree.heading('f4', text='性質')
        self.tree.heading('f5', text='開會地點')
        self.tree.heading('f6', text='股東會紀念品')
        self.tree.heading('f7', text='零股寄單')
        self.tree.heading('f8', text='股代')
        self.tree.heading('f9', text='股代電話')
        self.tree.heading('f10', text='是否到期')
        self.tree.column('no', width=40)
        self.tree.column('YER', width=100)
        self.tree.column('id', width=45)
        self.tree.column('name', width=100)
        self.tree.column('f1', width=100)
        self.tree.column('f2', width=80)
        self.tree.column('f3', width=80)
        self.tree.column('f4', width=60)
        self.tree.column('f5', width=100)
        self.tree.column('f6', width=140)
        self.tree.column('f7', width=60)
        self.tree.column('f8', width=100)
        self.tree.column('f9', width=100)
        self.tree.column('f10', width=60)
        self.tree.pack(side=tk.TOP)

        VScroll1 = tk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        VScroll1.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=VScroll1.set)

        self.tree.tag_configure("oddrow", background='#ff9', foreground='black')
        self.tree.tag_configure("evenrow", background='#99aa99', foreground='black')

        bottom_frame.pack()


if __name__ == "__main__":
    dsStockDividend.download_save_to_DataBase()
    dsMeeting.download_save_to_DataBase()

    window = Window()
    window.title("期末作業")
    window.geometry("1200x610+30+30")
    window.mainloop()

