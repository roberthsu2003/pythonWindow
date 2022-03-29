import dataSourse
import tkinter as tk
from tkinter import ttk
from tkinter import font
from datetime import datetime

class Window(tk.Tk):
    def __init__(self,banks):
        super().__init__()
        self.configure(background='grey50')
        titlefont = font.Font(family='Helvetica', size=20, weight='bold')
        titlelabel = ttk.Label(self, text='銀行即時外匯', font=titlefont, anchor=tk.CENTER)
        titlelabel.pack(fill=tk.X, pady=20)
        # 上方容器-----------start
        top_frame = tk.Frame(self, background='pink')
        # 左邊容器-----------start
        d = datetime.now()
        day = datetime.strftime(d,'%Y-%m-%d %H:%M:%S')
        left_label_frame = tk.LabelFrame(top_frame, text=f'更新時間 {day}', background='pink')

        # 左上容器-----------start
        left_top_frame = tk.Frame(left_label_frame, background='pink')
        bankLabel = ttk.Label(left_top_frame, text='銀行:',font=('arial',14))  # 要放在 left_label_frame 中
        bankLabel.pack(side=tk.LEFT, padx=(50,0))

        self.bankvar = tk.StringVar()  # 字串物件
        bank_combobox = ttk.Combobox(left_top_frame, textvariable=self.bankvar,font=('arial',14))
        # ttk.Combobox下拉式選單  #要放在 left_label_frame 中
        bank_combobox.pack(side=tk.LEFT)
        bank_combobox['values'] = banks
        bank_combobox.state(["readonly"])
        bank_combobox.bind('<<ComboboxSelected>>', self.bank_selected)  # 註冊 可抓到選單鍵連結
        left_top_frame.pack(side=tk.LEFT,pady=10)

        # 左上容器-----------end
        left_label_frame.pack(side=tk.LEFT, anchor=tk.N, fill=tk.X)
        # 左邊容器-----------end

        # 右邊容器-----------start
        right_label_frame = tk.LabelFrame(top_frame, text='幣別', background='orange')

        # 右上容器 button_frame-----------start
        def usdClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_usd()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        button_frame = tk.Frame(right_label_frame)
        usd_button = tk.Button(button_frame, text='美元', command=usdClick,font=('arial',12))  # 註冊 與 usdClick 連結
        usd_button.pack(side=tk.LEFT)

        def eurClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_eur()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        eur_button = tk.Button(button_frame, text='歐元', command=eurClick,font=('arial',12))
        eur_button.pack(side=tk.LEFT)

        def jpyClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_jpy()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        jpy_button = tk.Button(button_frame, text='日圓', command=jpyClick,font=('arial',12))
        jpy_button.pack(side=tk.LEFT)

        def audClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_aud()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        aud_button = tk.Button(button_frame, text='澳幣', command=audClick,font=('arial',12))
        aud_button.pack(side=tk.LEFT)

        def cnyClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_cny()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        cny_button = tk.Button(button_frame, text='人民幣', command=cnyClick,font=('arial',12))
        cny_button.pack(side=tk.LEFT)

        button_frame.pack(padx=50,pady=10)
        # 右上容器 button_frame-----------end
        # 右中容器 button2_frame-----------start
        def gbpClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_gbp()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        button2_frame = tk.Frame(right_label_frame)
        gbp_button = tk.Button(button2_frame, text='英鎊', command=gbpClick,font=('arial',12))  # 註冊 與 usdClick 連結
        gbp_button.pack(side=tk.LEFT)

        def sgdClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_sgd()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        sgd_button = tk.Button(button2_frame, text='新加坡幣', command=sgdClick,font=('arial',12))
        sgd_button.pack(side=tk.LEFT)

        def krwClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_krw()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        krw_button = tk.Button(button2_frame, text='韓元', command=krwClick,font=('arial',12))
        krw_button.pack(side=tk.LEFT)

        def zarClick():
            # 清空tree
            for i in self.tree.get_children():
                self.tree.delete(i)
            recodes = dataSourse.get_zar()
            for recode in recodes:
                self.tree.insert('', tk.END, values=recode)

        zar_button = tk.Button(button2_frame, text='南非幣', command=zarClick,font=('arial',12))
        zar_button.pack(side=tk.LEFT)
        button2_frame.pack(padx=50,pady=20)
        # 右中容器 button2_frame-----------end

        right_label_frame.pack(side=tk.RIGHT, fill=tk.X ,padx=(50, 0))
        # 右邊容器-----------end

        top_frame.pack(side=tk.TOP, anchor=tk.N)
        # 上方容器-----------end

        # 下方容器-----------start
        self.tree = ttk.Treeview(self, columns=('bank','coinTW', 'coin', 'nowbuy', 'nowsale', 'cashbuy', 'cashsale'), show='headings')
        self.tree.heading('bank', text='銀行')
        self.tree.heading('coinTW', text='幣別(中)')
        self.tree.heading('coin', text='幣別')
        self.tree.heading('nowbuy', text='銀行即期買入')
        self.tree.heading('nowsale', text='銀行即期賣出')
        self.tree.heading('cashbuy', text='銀行現金買入')
        self.tree.heading('cashsale', text='銀行現金賣出')

        self.tree.column('bank', width=100)
        self.tree.column('coinTW', width=100)
        self.tree.column('coin', width=100)
        self.tree.column('nowbuy', width=100)
        self.tree.column('nowsale', width=100)
        self.tree.column('cashbuy', width=100)
        self.tree.column('cashsale', width=100)
        self.tree.pack(side=tk.TOP)

    # 下方容器-----------end

    # Comboboxbind的事件
    def bank_selected(self, event):
        # 清空tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        selectedBank = self.bankvar.get()
        recodes = dataSourse.get_coin_info(selectedBank)
        for recode in recodes:
            self.tree.insert('', tk.END, values=recode)




if __name__ =='__main__':
    dataSourse.saveToDataBase()
    bank_name_list = dataSourse.get_bank_name()
    window = Window(bank_name_list)
    window.title('bank')
    window.mainloop()