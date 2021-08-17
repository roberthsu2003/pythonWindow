import time
import tkinter as tk
from .Covid19Info import Covid19Info
from tkinter import messagebox

# 彈窗
class PopupDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('搜尋結果')
        self.parent = parent  # 顯式地保留父視窗
        self.geometry("400x300+270+270")
        resultFrame = tk.Frame(self, relief=tk.GROOVE, pady=20, bd=2)
        # 第一行（5列）
        row1 = tk.Frame(resultFrame)
        row1.pack(fill="x")
        tk.Label(row1, width=15, text='序號：', font=("Courier",12), anchor=tk.E).pack(side=tk.LEFT)
        tk.Label(row1, width=15, text=str(self.parent.covid19Info.seq), font=("Courier",12)).pack(side=tk.LEFT)
        # 第二行
        row2 = tk.Frame(resultFrame)
        row2.pack(fill="x")
        tk.Label(row2, width=15, text='國家/地區名：', font=("Courier", 12), anchor=tk.E).pack(side=tk.LEFT)
        tk.Label(row2, width=15, text=self.parent.covid19Info.country_ch, font=("Courier", 12)).pack(side=tk.LEFT)
        # 第三行
        row3 = tk.Frame(resultFrame)
        row3.pack(fill="x")
        tk.Label(row3, width=15, text='英文名：', font=("Courier", 12), anchor=tk.E).pack(side=tk.LEFT)
        tk.Label(row3, width=15, text=self.parent.covid19Info.country_en, font=("Courier", 12)).pack(side=tk.LEFT)
        # 第四行
        row4 = tk.Frame(resultFrame)
        row4.pack(fill="x")
        tk.Label(row4, width=15, text='確診數：', font=("Courier", 12), anchor=tk.E).pack(side=tk.LEFT)
        tk.Label(row4, width=15, text=self.parent.covid19Info.cases, font=("Courier", 12)).pack(side=tk.LEFT)
        # 第五行
        row5 = tk.Frame(resultFrame)
        row5.pack(fill="x")
        tk.Label(row5, width=15, text='死亡數：', font=("Courier", 12), anchor=tk.E).pack(side=tk.LEFT)
        deathsLabel = tk.Label(row5, width=15, text=self.parent.covid19Info.deaths, font=("Courier", 12))
        deathsStr = self.parent.covid19Info.deaths
        deathsInt = int(deathsStr.replace(',', ''))
        if deathsInt > 100000:
            deathsLabel['fg'] = 'red'
        deathsLabel.pack(side=tk.LEFT)
        resultFrame.pack(pady=20)
        tk.Button(self, text="回主頁", font=("Couier",12), command=self.cancel, padx=20, pady=10).pack(side=tk.RIGHT,padx=50)

    def cancel(self):
        self.destroy()


# 主窗
class Window(tk.Tk):
    def __init__(self,callback,covid19Data):
        super().__init__()
        self.callback = callback  # callback 回呼函式
        self.covid19Data = covid19Data
        '''
        for covid in covid19Lst:
            print(covid.country_ch,covid.country_en,covid.cases,covid.deaths)
        '''
        self.geometry("900x650+100+50")
        titleFrame = tk.Frame(self)
        borderFrame = tk.Frame(titleFrame, bd = 3, relief=tk.GROOVE,padx=50,pady=10)
        tk.Label(borderFrame, text=" 全球 COVID-19 累積病例數與死亡數 ",font=("Courier", 20, "italic")).pack()
        localtime = time.localtime()
        self.updateDate = time.strftime("%Y-%m-%d", localtime)
        self.updateDateLabel = tk.Label(borderFrame, text="更新日期:"+self.updateDate,font=("Courier", 12),fg="green")
        self.updateDateLabel.pack(pady=(10,0))
        self.inputFrame = tk.Frame(borderFrame,padx=10)
        tk.Label(self.inputFrame, text="國家/地區:", font=("Courier", 12)).pack(side=tk.LEFT,pady=(10,0))
        self.areaEntry = tk.Entry(self.inputFrame, textvariable=tk.StringVar(), bd=5, font=("Courier", 12))
        self.areaEntry.pack(side=tk.LEFT,pady=(10,0))
        tk.Button(self.inputFrame, text="搜尋", padx=10, font=("Courier", 12), \
                  command=self.setup_config).pack(side=tk.LEFT,pady=(10,0))
        tk.Button(self.inputFrame,text="更新",padx=10,pady=5,font=("Courier", 12, "bold"),\
                  command=self.button_handler).pack(padx=(150,0),pady=(10,0),side=tk.RIGHT)
        self.inputFrame.pack()
        borderFrame.pack()
        titleFrame.pack(padx=10,pady=10)

        # 建立下方的 frame
        self.createDisplayFrame(self.covid19Data)



    def createDisplayFrame(self,covid19Data):
        # 建立 bottomRootFrame
        self.bottomRootFrame = tk.Frame(self)
        # 建立canvas
        canvas = tk.Canvas(self.bottomRootFrame, width=800, height=400)
        #canvasScrollbar
        canvasScrollBar = tk.Scrollbar(self.bottomRootFrame, orient="vertical", command=canvas.yview)
        canvasScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        # 下方的 frame
        self.displayFrame = tk.Frame(canvas, bg='#ccc')
        self.displayFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                # scrollregion=canvas.bbox("all")
                scrollregion=canvas.bbox(tk.ALL)
            )
        )
        # covid19Lst = covid19Data
        if not covid19Data is None:
            for index,covid in enumerate(covid19Data):
                tk.Label(self.displayFrame, text=covid.seq,font=("Courier", 11), bg='#ccc').grid(row=index, column=0,sticky=tk.E,padx=10)
                tk.Label(self.displayFrame, text=covid.country_ch,font=("Courier", 11), bg='#ccc').grid(row=index, column=1,sticky=tk.W)
                tk.Label(self.displayFrame, text=covid.country_en,font=("Courier", 11), bg='#ccc').grid(row=index, column=2,sticky=tk.W)
                tk.Label(self.displayFrame, text=covid.cases,font=("Courier", 11), bg='#ccc').grid(row=index, column=3,sticky=tk.E)
                deathsLabel = tk.Label(self.displayFrame, text=covid.deaths, bg='#ccc')
                deathsStr = covid.deaths
                deathsInt = int(deathsStr.replace(',',''))
                if deathsInt > 100000:
                    deathsLabel['fg'] = 'red'
                deathsLabel.grid(row=index, column=4,sticky=tk.E,padx=50)
        # self.displayFrame.pack()
        canvas.create_window((0,0),window=self.displayFrame, anchor=tk.NW)
        # canvas.config(yscrollcommand=canvasScrollBar.set)
        canvas.pack(side=tk.LEFT)
        self.bottomRootFrame.pack(padx=10,pady=10)
        self.designLabel = tk.Label(self, text="Designed By Fiona Wu 2021/08/08", font=("Courier", 12), fg='blue')
        self.designLabel.pack(side=tk.RIGHT, padx=50)

    # 設定引數
    def setup_config(self):
        self.covid19Info = Covid19Info()
        area = self.areaEntry.get()
        if area is None or len(area)==0:
            messagebox.showinfo("訊息", "請輸入國家/地區 !")
        else:
            for covid in self.covid19Data:
                # print(covid.seq, covid.country_ch, len(covid.country_ch))
                if covid.country_ch == area or covid.country_en == area:
                    self.covid19Info.seq = covid.seq
                    self.covid19Info.country_ch = covid.country_ch
                    self.covid19Info.country_en = covid.country_en
                    self.covid19Info.cases = covid.cases
                    self.covid19Info.deaths = covid.deaths
                    break


            if not self.covid19Info.country_ch is None:
                # print('message',self.covid19Info.country_ch)
                pw = PopupDialog(self)
                self.wait_window(pw)  # 這一句很重要！！！
                return
            else:
                # print('area=',area)
                messagebox.showinfo("訊息" ,"查無 " + area + " 國家/地區 !")

    def button_handler(self):
        self.callback() # 執行 回呼函式

