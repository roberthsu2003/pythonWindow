from tkinter import ttk
import tkinter as tk
from tkinter.simpledialog import Dialog

class YoubikeTreeView(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        #------設定欄位名稱---------------
        # self.heading('sno',text='ID')
        self.heading('sna',text='站點名稱')
        self.heading('sarea',text='行政區')
        self.heading('mday',text='更新時間')
        self.heading('ar',text='地址')
        self.heading('tot',text='總車輛數')
        self.heading('sbi',text='可借')
        self.heading('bemp',text='可還')

        #----------設定欄位寬度------------
        # self.column('sno',width=100)
        self.column('sna',width=265)
        self.column('sarea',width=90)
        self.column('mday',width=150)
        self.column('ar',width=300)
        self.column('tot',width=70)
        self.column('sbi',width=50)
        self.column('bemp',width=50)

        #----------bind button1-------
        self.bind('<ButtonRelease-1>', self.selectedItem)

    def update_content(self,site_datas)->None:
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
        # self.sno = data[0] # id欄位
        # self.sna = data[1]
        # self.sarea = data[2]
        # self.mday = data[3]
        # self.ar = data[4]
        # self.tot = data[5]
        # self.sbi = data[6]
        # self.bemp = data[7]
        
        self.sna = data[0]
        self.sarea = data[1]
        self.mday = data[2]
        self.ar = data[3]
        self.tot = data[4]
        self.sbi = data[5]
        self.bemp = data[6]
        super().__init__(parent,**kwargs)


    def body(self, master):        
        '''
        override body,可以自訂body的外觀內容
        '''
        ListFrame = tk.Frame(master)
        ListFrame.pack(padx=5,pady=5)
        # tk.Label(ListFrame,text="ID").grid(column=0, row=0,sticky='W')
        # tk.Label(ListFrame,text="站點名稱").grid(column=0, row=1,sticky='W')
        # tk.Label(ListFrame,text="行政區").grid(column=0, row=2,sticky='W')
        # tk.Label(ListFrame,text="更新時間").grid(column=0, row=3,sticky='W')
        # tk.Label(ListFrame,text="地址").grid(column=0, row=4,sticky='W')
        # tk.Label(ListFrame,text="總量").grid(column=0, row=5,sticky='W')
        # tk.Label(ListFrame,text="可借").grid(column=0, row=6,sticky='W')
        # tk.Label(ListFrame,text="可還").grid(column=0, row=7,sticky='W')
        tk.Label(ListFrame,text="站點名稱").grid(column=0, row=0,sticky='W')
        tk.Label(ListFrame,text="行政區").grid(column=0, row=1,sticky='W')
        tk.Label(ListFrame,text="更新時間").grid(column=0, row=2,sticky='W')
        tk.Label(ListFrame,text="地址").grid(column=0, row=3,sticky='W')
        tk.Label(ListFrame,text="總量").grid(column=0, row=4,sticky='W')
        tk.Label(ListFrame,text="可借").grid(column=0, row=5,sticky='W')
        tk.Label(ListFrame,text="可還").grid(column=0, row=6,sticky='W')

        # snoVar = tk.StringVar()
        # snoVar.set(self.sno)
        # tk.Entry(ListFrame,textvariable=snoVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=0,sticky='E')

        snaVar = tk.StringVar()
        snaVar.set(self.sna)
        # tk.Entry(ListFrame,textvariable=snaVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=1,sticky='E')
        tk.Entry(ListFrame,textvariable=snaVar,state='disabled',width=42,justify=tk.LEFT).grid(column=1,row=0,sticky='E')

        sareaVar = tk.StringVar()
        sareaVar.set(self.sarea)
        # tk.Entry(ListFrame,textvariable=sareaVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=2,sticky='E')
        tk.Entry(ListFrame,textvariable=sareaVar,state='disabled',width=42,justify=tk.LEFT).grid(column=1,row=1,sticky='E')

        mdayVar = tk.StringVar()
        mdayVar.set(self.mday)
        # tk.Entry(ListFrame,textvariable=mdayVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=3,sticky='E')
        tk.Entry(ListFrame,textvariable=mdayVar,state='disabled',width=42,justify=tk.LEFT).grid(column=1,row=2,sticky='E')

        arVar = tk.StringVar()
        arVar.set(self.ar)
        # tk.Entry(ListFrame,textvariable=arVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=4,sticky='E')
        tk.Entry(ListFrame,textvariable=arVar,state='disabled',width=42,justify=tk.LEFT).grid(column=1,row=3,sticky='E')

        totVar = tk.StringVar()
        totVar.set(self.tot)
        # tk.Entry(ListFrame,textvariable=totVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=5,sticky='E')
        tk.Entry(ListFrame,textvariable=totVar,state='disabled',width=42,justify=tk.LEFT).grid(column=1,row=4,sticky='E')

        sbiVar = tk.StringVar()
        sbiVar.set(self.sbi)
        # tk.Entry(ListFrame,textvariable=sbiVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=6,sticky='E')
        tk.Entry(ListFrame,textvariable=sbiVar,state='disabled',width=42,justify=tk.LEFT).grid(column=1,row=5,sticky='E')
    
        bempVar = tk.StringVar()
        bempVar.set(self.bemp)
        # tk.Entry(ListFrame,textvariable=bempVar,state='disabled',width=42,justify=tk.RIGHT).grid(column=1,row=7,sticky='E')
        tk.Entry(ListFrame,textvariable=bempVar,state='disabled',width=42,justify=tk.LEFT).grid(column=1,row=6,sticky='E')

        self.resizable(width=False,height=False)

    def buttonbox(self):
        '''
        override buttonbox,可以自訂body的外觀內容
        '''
        boxFrame = tk.Frame(self)

        w = tk.Button(boxFrame, text="確認", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(padx=5, pady=(5,15))      

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        boxFrame.pack()