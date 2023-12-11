'''
    - 提供關注中華職棒的使用者，透過視窗快速查找指定球員的相關數據
    - 搭配圖表分析了解球員進階數據與全聯盟平均之比較
'''

import tkinter as tk
from tkinter import ttk
from cpbl_treeview import cpblTreeView
from cpbl_treeview import player
from tkinter import messagebox
import datasource
from PIL import Image, ImageTk
import ttkbootstrap as ttk

class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        try:
            datasource.update_sqlite_data()
        except Exception: 
            messagebox.showerror('錯誤', '網路不正常\n將關閉應用程式\n請稍後再試') 
            self.destroy() 

#-------------------------------建立介面--------------------------------------------
#------------------------------最上面的標題---------------------------------------
        style = ttk.Style("cyborg")
        topFrame =tk.Frame(self,relief=tk.GROOVE,borderwidth=1)
        tk.Label(topFrame,text='中華職棒球員資料',font=('arial,40'),bg='#333333',fg='#FFFFFF',pady=20).pack(fill='both', pady=5, padx=5,ipadx=5,ipady=5,expand=True)
        topFrame.pack(pady=5,expand=True)

#----------------------------建立上層介面------------------------------------
        container = ttk.LabelFrame(self,text='球員資料',relief=tk.GROOVE,borderwidth=1)
        container.pack(fill='y',ipadx=10,ipady=10,padx=10,pady=10,expand=True)

#------------------------------球員個人資料、PR數據---------------------------------------
        
        photoFrame = ttk.LabelFrame(container,text='球員照片',relief=tk.GROOVE,borderwidth=1)
        photoFrame.pack(side='left', anchor="n", expand=True, fill='both',ipadx=5,ipady=5,padx=5,pady=5)
        self.tk_img = None

        self.infoFrame = ttk.LabelFrame(container, text='球員資料', relief=tk.GROOVE, borderwidth=1)
        self.infoFrame.pack(side='left', anchor="n", fill='y',ipadx=5,ipady=5,padx=5,pady=5, expand=True)

        self.player_data = ttk.LabelFrame(container, text='進階數據', relief=tk.GROOVE, borderwidth=1)
        self.player_data.pack(side='left', anchor="n", fill='y',ipadx=5,ipady=5,padx=5,pady=5, expand=True)

        prframe = ttk.LabelFrame(container, text='奪三振率(K9值)&防禦率(ERA)', relief=tk.GROOVE, borderwidth=1)
        prframe.pack(side='left', anchor="n", fill='both',ipadx=5,ipady=5,padx=5,pady=5, expand=True)
        
        #當滑鼠左鍵點擊時啟動球員詳細資料視窗
        def info(event):  

            #球員基本資料
            self.update_idletasks()
            for widget in self.infoFrame.winfo_children():
                widget.destroy()

            data = player.list_info()
            Team_info = data[1]
            Name_info = data[3]
            B_t_info = data[18]                 
            Number_info = data[19]
            Ht_wt_info = data[20]
            Born_info = data[21]

            Team = tk.Label(self.infoFrame, text='所屬球隊：').grid(row=0, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            Name = tk.Label(self.infoFrame, text='球員姓名：').grid(row=1, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            Number = tk.Label(self.infoFrame, text='背號：').grid(row=2, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            B_t = tk.Label(self.infoFrame, text='投打習慣：').grid(row=3, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            Ht_wt = tk.Label(self.infoFrame, text='身高體重：').grid(row=4, column=0,sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            Born = tk.Label(self.infoFrame, text='生日：').grid(row=5, column=0, sticky='w',ipadx=5,ipady=5,padx=2,pady=2)

            TeamVar = tk.StringVar()
            TeamVar.set(Team_info)
            print(f'Team{Team_info}')
            tk.Entry(self.infoFrame,textvariable=TeamVar,state='normal' ).grid(column=1,row=0)
                
            NameVar = tk.StringVar()
            NameVar.set(Name_info)
            tk.Entry(self.infoFrame,textvariable=NameVar,state='normal' ).grid(column=1,row=1)

            NumberVar = tk.StringVar()
            NumberVar.set(Number_info)
            tk.Entry(self.infoFrame,textvariable=NumberVar,state='normal' ).grid(column=1,row=2)

            B_tVar = tk.StringVar()
            B_tVar.set(B_t_info)
            tk.Entry(self.infoFrame,textvariable=B_tVar,state='normal' ).grid(column=1,row=3)

            Ht_wtVar = tk.StringVar()
            Ht_wtVar.set(Ht_wt_info)
            tk.Entry(self.infoFrame,textvariable=Ht_wtVar,state='normal' ).grid(column=1,row=4)

            BornVar = tk.StringVar()
            BornVar.set(Born_info)
            tk.Entry(self.infoFrame,textvariable=BornVar,state='normal' ).grid(column=1,row=5)
            
            #球員詳細資料
            for widget in self.player_data.winfo_children():
                widget.destroy()

            print(f'跑到{data}')
            IP_info = data[11]
            SV_info = data[9]
            HLD_info = data[10]                 
            H_info = data[13]
            HR_info = data[14]
            BB_info = data[15]


            IP = tk.Label(self.player_data, text='有效局數：').grid(row=0, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            SV = tk.Label(self.player_data, text='救援成功：').grid(row=1, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            HLD = tk.Label(self.player_data, text='中繼成功：').grid(row=2, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            H = tk.Label(self.player_data, text='被安打數：').grid(row=3, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            HR = tk.Label(self.player_data, text='被全壘打數：').grid(row=4, column=0, sticky='w', ipadx=5,ipady=5,padx=2,pady=2)
            BB = tk.Label(self.player_data, text='保送數：').grid(row=5, column=0,sticky='w', ipadx=5,ipady=5,padx=2,pady=2)


            IPVar = tk.StringVar()
            IPVar.set(IP_info)
            print(f'Team{IP_info}')
            tk.Entry(self.player_data,textvariable=IPVar,state='normal' ).grid(column=1,row=0)
                
            SVVar = tk.StringVar()
            SVVar.set(SV_info)
            tk.Entry(self.player_data,textvariable=SVVar,state='normal' ).grid(column=1,row=1)

            HLDVar = tk.StringVar()
            HLDVar.set(HLD_info)
            tk.Entry(self.player_data,textvariable=HLDVar,state='normal' ).grid(column=1,row=2)

            HVar = tk.StringVar()
            HVar.set(H_info)
            tk.Entry(self.player_data,textvariable=HVar,state='normal' ).grid(column=1,row=3)

            HRVar = tk.StringVar()
            HRVar.set(HR_info)
            tk.Entry(self.player_data,textvariable=HRVar,state='normal' ).grid(column=1,row=4)

            BBVar = tk.StringVar()
            BBVar.set(BB_info)
            tk.Entry(self.player_data,textvariable=BBVar,state='normal' ).grid(column=1,row=5)



            # 抓取球員照片
            for widget in photoFrame.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.destroy()
            
            name = player.player_name()
            photo_path = f'./img/{name}.jpg'
            img = Image.open(photo_path)

            # 調整圖片大小為 120x160
            img = img.resize((120, 160), Image.BILINEAR)

            # 將圖片轉換為 Tkinter PhotoImage 對象，使用實例變數
            self.tk_img = ImageTk.PhotoImage(img)

            # 創建一個 Canvas 並在其中放入圖片
            canvas = tk.Canvas(photoFrame, width=120, height=160)
            canvas.pack(side='top', fill='x', expand=True)

            # 計算圖片在 Canvas 中的座標
            img_width, img_height = 120, 160
            x = ((canvas.winfo_reqwidth() - img_width) / 2)+10
            y = (canvas.winfo_reqheight() - img_height) / 2

            # 在 Canvas 中創建圖片
            canvas.create_image(x, y, anchor='nw', image=self.tk_img)

            for widget in prframe.winfo_children():
                widget.destroy()
            
            canvasphoto = player.pr_value(prframe)


##-----------------------------建立隊伍按鈕-----------------------------------

        middle1Frame = ttk.LabelFrame(self,text='選擇球隊',relief=tk.GROOVE,borderwidth=1)
        tk.Label(middle1Frame,text='選擇球隊').pack
        middle1Frame.pack(side='top',fill='x', ipadx=10,ipady=10,padx=10,pady=10, expand=True)

        def team_search(event:None, word:str):
            print(word)
            rows = datasource.search_by_team(event=None, word=word)
            self.cpblTreeView.update_content(site_datas=rows)
            self.bind('<ButtonRelease-1>',info)

        ttk.Button(middle1Frame, text='中信兄弟', style='info', command=lambda: team_search(event=None, word='中信')).pack(ipadx=25, ipady=10, side='left', expand='Yes')

        ttk.Button(middle1Frame, text='樂天桃猿',bootstyle='Danger',command=lambda: team_search(event=None,word='樂天')).pack(ipadx=25, ipady=10, side='left',expand='Yes')
        ttk.Button(middle1Frame, text='統一7-ELEVEn獅',bootstyle='Warning',command=lambda: team_search(event=None,word='統一')).pack(ipadx=25, ipady=10, side='left',expand='Yes')
        ttk.Button(middle1Frame, text='富邦悍將',command=lambda: team_search(event=None,word='富邦')).pack(ipadx=25, ipady=10, side='left',expand='Yes')
        ttk.Button(middle1Frame, text='味全龍',bootstyle='success',command=lambda: team_search(event=None,word='味全')).pack(ipadx=25, ipady=10, side='left',expand='Yes')


#------------------------------建立treeView-----------------------------------------
        bottomFrame = tk.Frame(self)
        self.cpblTreeView = cpblTreeView(bottomFrame,columns=('Year','Team Name','ID','Name','G', 'GS', 'GR', 'W', 'L', 'SV', 'HLD', 'IP', 'BF', 'H', 'HR', 'BB', 'SO', 'ER'),show="headings",height=20)
        #設定捲動軸 
        self.cpblTreeView.pack(side='left', fill='both', expand=True)
        vsb = ttk.Scrollbar(bottomFrame, orient='vertical',command=self.cpblTreeView.yview)
        vsb.pack(side='right',fill='y', expand=True)
        self.cpblTreeView.configure(yscrollcommand=vsb.set)
        bottomFrame.pack(pady=(0,30), padx=20) #pady=(與上段距離，與下段距離)  
#-----------------------------更新treeView資料--------------------------------------
        lastest_data = datasource.lastest_datetime_data()               
        self.cpblTreeView.update_content(site_datas=lastest_data)
        self.bind('<ButtonRelease-1>',info)

#-----------------------------主程式定期自動更新資料--------------------------------------
def main():     
    def update_data(w:Window)->None:   
        print('資訊更新')

    window = Window() 
    window.title('中華職棒球員資料查詢')
    window.resizable(width=True,height=True) 
    update_data(window)
    window.wait_window() 



if __name__ == '__main__':
    main()