from tkinter import ttk
import tkinter as tk
from tkinter.simpledialog import Dialog

class YoubikeTreeView(ttk.Treeview):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.parent = parent
        #------設定欄位名稱---------------
        self.heading('sna',text='站點名稱')
        self.heading('mday',text='更新時間')
        self.heading('sarea',text='行政區')
        self.heading('ar',text='地址')
        self.heading('tot',text='總車輛數')
        self.heading('sbi',text='可借')
        self.heading('bemp',text='可還')

        #----------設定欄位寬度------------
        self.column('sna',width=200)
        self.column('mday',width=150)
        self.column('sarea',width=50)
        self.column('ar',width=300)
        self.column('tot',width=50)
        self.column('sbi',width=50)
        self.column('bemp',width=50)

        #----------bind button1-------
        self.bind('<ButtonRelease-1>', self.selectedItem)

    def update_content(self,site_datas):
        '''
        更新內容
        '''
        #清除所有內容
        for i in self.get_children():
            self.delete(i)
        
        for index,site in enumerate(site_datas):
            self.insert('','end',text=f"abc{index}",values=site)


    def selectedItem(self,event):
        selectedItem = self.focus()
        print(selectedItem)
        data_dict = self.item(selectedItem)
        data_list = data_dict['values']
        title = data_list[0]
        detail = ShowDetail(self.parent,data=data_list,title=title)
        


class ShowDetail(Dialog):
    def __init__(self,parent,data,**kwargs):
        self.sna = data[0]
        self.mday = data[1]
        self.sarea = data[2]
        self.ar = data[3]
        self.tot = data[4]
        self.sbi = data[5]
        self.bemp = data[6]
        super().__init__(parent,**kwargs)
        

    def body(self, master):        
        '''
        override body,可以自訂body的外觀內容
        '''
        mainFrame = tk.Frame(master)
        mainFrame.pack(padx=100,pady=100)
        tk.Label(mainFrame,text="站點名稱").grid(column=0, row=0)
        tk.Label(mainFrame,text="更新時間").grid(column=0, row=1)
        tk.Label(mainFrame,text="行政區").grid(column=0, row=2)
        tk.Label(mainFrame,text="地址").grid(column=0, row=3)
        tk.Label(mainFrame,text="總量").grid(column=0, row=4)
        tk.Label(mainFrame,text="可借").grid(column=0, row=5)
        tk.Label(mainFrame,text="可還").grid(column=0, row=6)
        snaVar = tk.StringVar()
        snaVar.set(self.sna)
        tk.Entry(mainFrame,textvariable=snaVar,state='disabled').grid(column=1,row=0)

        mdayVar = tk.StringVar()
        mdayVar.set(self.mday)
        tk.Entry(mainFrame,textvariable=mdayVar,state='disabled').grid(column=1,row=1)

        sareaVar = tk.StringVar()
        sareaVar.set(self.sarea)
        tk.Entry(mainFrame,textvariable=sareaVar,state='disabled').grid(column=1,row=2)

        arVar = tk.StringVar()
        arVar.set(self.ar)
        tk.Entry(mainFrame,textvariable=arVar,state='disabled').grid(column=1,row=3)

        totVar = tk.StringVar()
        totVar.set(self.tot)
        tk.Entry(mainFrame,textvariable=totVar,state='disabled').grid(column=1,row=4)

        sbiVar = tk.StringVar()
        sbiVar.set(self.sbi)
        tk.Entry(mainFrame,textvariable=sbiVar,state='disabled').grid(column=1,row=5)

        bempVar = tk.StringVar()
        bempVar.set(self.bemp)
        tk.Entry(mainFrame,textvariable=bempVar,state='disabled').grid(column=1,row=6)

    def buttonbox(self):
        '''
        override buttonbox,可以自訂body的外觀內容
        '''
        box = tk.Frame(self)

        w = tk.Button(box, text="確認", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(padx=5, pady=(5,20))      

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

