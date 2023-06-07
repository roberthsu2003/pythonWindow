import dataSourceML
import dataSource
import io
#from io import StringIO
import csv
import pandas as pd                                                  #pip install pandas
import tkinter as tk
from tkinter import ttk
#import seaborn as sns; sns.set()                                     #pip install seaborn  
import seaborn as sns 
import matplotlib.pyplot as plt                                      #pip install matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import MultipleLocator



plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False

class Window(tk.Tk):
    def __init__(self,atmMLData):
        super().__init__()
        self.atmMLData = atmMLData
        

        self.pie11 = None
        self.pie21 = None
        self.scatter12 = None
        self.scatter22 = None        
        self.heatmap03 = None
        self.heatmap13 = None
        self.dbsAllTree = None
        self.dbsCountyTree = None

        self.BankRw0Cn1RadiusDbscanFrame = None

    # self.Mainframe:------------------------------------------------------------------------
        self.mainFrame = ttk.Frame(self)
        self.mainFrame.pack(fill=tk.X,padx=10,pady=3)
        
        treeStyle = ttk.Style() 
        treeStyle.configure('Treeview', foreground="Orange")   
        #treeStyle.configure('Treeview', rowheight=18)         
        #ttkStyle = ttk.Style()
        #ttkStyle.theme_use('clam')          #只有clam有bordercolor效果('clam', 'alt', 'default', 'classic')    
        #ttkStyle.configure('BLUE.TLabelframe.Label', foreground='blue', font=("TkDefaultFont", 9, "bold"))    
        #ttkStyle.configure('BLUE.TLabelframe.Label', foreground='blue')    

    # ATM同業競爭性 : 據點市占 ------------------------------------------------------  
        ## bankRw0Cn0Frame, bankTree -----------------------------
        self.bankRw0Cn0Frame = ttk.LabelFrame(self.mainFrame,text='ATM同業競爭 - 據點市占 : ')
        self.bankRw0Cn0Frame.grid(row=0, column=0, padx=10, pady=(4,0), sticky=tk.W)

        # build ttk.Treeview        
        columns = ('#1', '#2', '#3', '#4', '#5')
        self.bankTree = ttk.Treeview(self.bankRw0Cn0Frame, columns=columns, show='headings', height=8)
        ### define headings
        self.bankTree.heading('#1', text='排名')
        self.bankTree.column('#1', minwidth=0, width=33, anchor='center')
        self.bankTree.heading('#2', text='金融機構')
        self.bankTree.column('#2', minwidth=0, width=75, anchor='center')
        self.bankTree.heading('#3', text='設點數')
        self.bankTree.column('#3', minwidth=0, width=60, anchor="e")
        self.bankTree.heading('#4', text='占全體%')
        self.bankTree.column('#4', minwidth=0, width=65, anchor="e")   
        self.bankTree.heading('#5', text='累積%')
        self.bankTree.column('#5', minwidth=0, width=65, anchor="e")     
        self.bankTree.pack(side=tk.LEFT,padx=10,pady=(2,4))

        ### build ttk.scrollBar
        scrollBar = ttk.Scrollbar(self.bankRw0Cn0Frame,orient='vertical',command=self.bankTree.yview)
        scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        self.bankTree.configure(yscrollcommand=scrollBar.set)
        
        ### produce bankList
        groupBankUnits = dataSourceML.atmSelectedList(self.atmMLData)   
        self.groupBankList = groupBankUnits.atmBankList()
        #print(self.groupBankList)
        
        for i in range(self.groupBankList['bankbrifname'].size):
            self.bankTree.insert('', tk.END, 
                             values=[self.groupBankList.index[i]+1,self.groupBankList.iloc[i,0],self.groupBankList.iloc[i,1],self.groupBankList.iloc[i,2],self.groupBankList.iloc[i,3]],tags=self.groupBankList.iloc[i,0]
                            ) 
        self.bankTree.bind('<<TreeviewSelect>>',self.bankTreeSelected) 
        
        ## BankRw0Cn1DbscanFrame, BankTree -------
        self.BankRw0Cn1DbscanFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.BankRw0Cn1DbscanFrame.grid(row=0, column=1, padx=(10,10), pady=(4,0), sticky=tk.E)        
        
        ## BankRw0Cn2DbscanFrame, DbscanTree ----------------------------        
        self.BankRw0Cn2DbscanFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.BankRw0Cn2DbscanFrame.grid(row=0, column=2, padx=(0,10), pady=(4,0), sticky=tk.W)        
        
        ## BankRw0Cn3GraphFrame, DbscanTree -----------------------        
        self.BankRw0Cn3GraphFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.BankRw0Cn3GraphFrame.grid(row=0, column=3, padx=(0,10), pady=(4,0), sticky=tk.W)
        

   
    # ATM同業競爭性 : 裝設縣市 ------------------------------------------------------------ 
        ## countyOfBankRw1Cn0Frame, countyOfBankTree -------------
        self.countyOfBankRw1Cn0Frame = ttk.LabelFrame(self.mainFrame,text='ATM同業策略 - 區域佈局 : ')
        self.countyOfBankRw1Cn0Frame.grid(row=1, column=0, padx=10, pady=(4,0), sticky=tk.W)

        # build ttk.Treeview
        columns = ('#1', '#2', '#3', '#4', '#5')
        self.countyOfBankTree = ttk.Treeview(self.countyOfBankRw1Cn0Frame, columns=columns, show='headings', height=8)
        ### define headings
        self.countyOfBankTree.heading('#1', text='排名')
        self.countyOfBankTree.column('#1', minwidth=0, width=33, anchor='center')
        self.countyOfBankTree.heading('#2', text='裝設縣市')
        self.countyOfBankTree.column('#2', minwidth=0, width=75, anchor='center')
        self.countyOfBankTree.heading('#3', text='設點數')
        self.countyOfBankTree.column('#3', minwidth=0, width=60, anchor="e")
        self.countyOfBankTree.heading('#4', text='占機構%')
        self.countyOfBankTree.column('#4', minwidth=0, width=65, anchor="e")     
        self.countyOfBankTree.heading('#5', text='累積%')
        self.countyOfBankTree.column('#5', minwidth=0, width=65, anchor="e")    
        self.countyOfBankTree.pack(side=tk.LEFT,padx=10,pady=(2,4))

        ### build ttk.scrollBar
        scrollBar = ttk.Scrollbar(self.countyOfBankRw1Cn0Frame,orient='vertical',command=self.countyOfBankTree.yview)
        scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        self.countyOfBankTree.configure(yscrollcommand=scrollBar.set) 
        
        ## countyOfBankRw1Cn2GraphFrame---------------------------
        self.countyOfBankRw1Cn2GraphFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.countyOfBankRw1Cn2GraphFrame.grid(row=1, column=2, padx=(0,10), pady=(4,0), sticky=tk.W)

        ## countyOfBankRw1Cn1GraphFrame---------------------------
        self.countyOfBankRw1Cn1GraphFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.countyOfBankRw1Cn1GraphFrame.grid(row=1, column=1, padx=(10,10), pady=(4,0), sticky=tk.W)        
        
        ## countyOfBankRw1Cn3GraphFrame---------------------------
        self.countyOfBankRw1Cn3GraphFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.countyOfBankRw1Cn3GraphFrame.grid(row=1, column=3, padx=(0,10), pady=(4,0), sticky=tk.W)

   
    # ATM同業競爭性 : 裝設地點 ----------------------------------------------------------     
        ## placeOfBankRw2Cn0Frame, placeOfBankTree ---------------   
        self.placeOfBankRw2Cn0Frame = ttk.LabelFrame(self.mainFrame,text='ATM同業策略 - 異業結盟 : ')
        self.placeOfBankRw2Cn0Frame.grid(row=2, column=0, padx=10, pady=(4,0), sticky=tk.W)

        # build ttk.Treeview
        columns = ('#1', '#2', '#3', '#4', '#5')
        self.placeOfBankTree = ttk.Treeview(self.placeOfBankRw2Cn0Frame, columns=columns, show='headings', height=8)
        ### define headings
        self.placeOfBankTree.heading('#1', text='排名')
        self.placeOfBankTree.column('#1', minwidth=0, width=33, anchor='center')
        self.placeOfBankTree.heading('#2', text='裝設地點')
        self.placeOfBankTree.column('#2', minwidth=0, width=75, anchor='w')
        self.placeOfBankTree.heading('#3', text='設點數')
        self.placeOfBankTree.column('#3', minwidth=0, width=60, anchor="e")
        self.placeOfBankTree.heading('#4', text='占機構%')
        self.placeOfBankTree.column('#4', minwidth=0, width=65, anchor="e")     
        self.placeOfBankTree.heading('#5', text='累積%')
        self.placeOfBankTree.column('#5', minwidth=0, width=65, anchor="e")    
        self.placeOfBankTree.pack(side=tk.LEFT,padx=10,pady=(2,4))

        ### build ttk.scrollBar
        scrollBar = ttk.Scrollbar(self.placeOfBankRw2Cn0Frame,orient='vertical',command=self.placeOfBankTree.yview)
        scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        self.placeOfBankTree.configure(yscrollcommand=scrollBar.set) 

        ## placeOfBankRw2Cn2GraphFrame ------------------------
        self.placeOfBankRw2Cn2GraphFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.placeOfBankRw2Cn2GraphFrame.grid(row=2, column=2, padx=(0,10), pady=(4,0), sticky=tk.W)

        ## placeOfBankRw2Cn1GraphFrame -------------------------
        self.placeOfBankRw2Cn1GraphFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.placeOfBankRw2Cn1GraphFrame.grid(row=2, column=1, padx=(10,10), pady=(4,0), sticky=tk.W)

        ## countyOfRw2Cn3DbscanFrame :DBSCAN分組說明-------------
        self.countyOfRw2Cn3DbscanFrame = ttk.LabelFrame(self.mainFrame,text='')
        self.countyOfRw2Cn3DbscanFrame.grid(row=2, column=3, padx=(0,10), pady=(4,0), sticky=tk.E)   


    # FUNCTIONS --------------------------------------------------------------------------------------------------------------------
    # Rw1, 
    def bankTreeSelected(self,event):    
        # prcessing bankTree-----------------------------------------------------------
        selectedTree = event.widget 
        ### get selectedBank
        itemTage = selectedTree.selection()[0]      #selectedTree.selection()=('I005',)
        itemDic = selectedTree.item(itemTage)       #{'text': '', 'image': '', 'values': [812, '台新東高雄', ...], 'open': 0, 'tags': [5831]}
        self.selectedBank = itemDic['tags'][0]
        #print(self.selectedBank)
        ### modify configure of bankRw0Cn0Frame      
        self.bankRw0Cn0Frame.configure(text=f'ATM同業競爭 - 據點市占 :「{self.selectedBank} - 全台」')


        # Rw1
        # prcessing Tree: countyOfBank--------------------------------------------------
        ### modify countyOfBankRw1Cn0Frame
        self.countyOfBankRw1Cn0Frame.configure(text=f'ATM同業策略 - 區域佈局 :「{self.selectedBank}」')        
        ### prcessing countyOfBankTree
        groupCountOfBank = dataSourceML.atmSelectedList(self.atmMLData,selectedBank=self.selectedBank,selectedItem='county')   
        self.groupCountyOfBankList = groupCountOfBank.atmBankListOfItem()
        #print(self.groupCountyOfBankList)        
        for item in self.countyOfBankTree.get_children():
            self.countyOfBankTree.delete(item)         
        for i in range(self.groupCountyOfBankList['county'].size):
            self.countyOfBankTree.insert('', tk.END, 
                             values=[self.groupCountyOfBankList.index[i]+1,self.groupCountyOfBankList.iloc[i,0],self.groupCountyOfBankList.iloc[i,1],self.groupCountyOfBankList.iloc[i,2],self.groupCountyOfBankList.iloc[i,3]],tags=self.groupCountyOfBankList.iloc[i,0]
                            ) 
        self.countyOfBankTree.bind('<<TreeviewSelect>>',self.countyOfBankTreeSelected)  

        ### delete countyOfBankRw1Cn2GraphFrame       
        self.countyOfBankRw1Cn2GraphFrame.configure(text='') 
        if self.pie11:
            self.pie11.get_tk_widget().destroy()
            self.pie11 = None        
        ### delete countyOfBankRw1Cn1GraphFrame       
        self.countyOfBankRw1Cn1GraphFrame.configure(text='') 
        if self.scatter12:
            self.scatter12.get_tk_widget().destroy()
            self.scatter12 = None     
        ### delete countyOfBankRw1Cn3GraphFrame       
        self.countyOfBankRw1Cn3GraphFrame.configure(text='') 
        if self.heatmap13:
            self.heatmap13.get_tk_widget().destroy()
            self.heatmap13 = None         
        ### delete BankRw0Cn3GraphFrame     
        self.BankRw0Cn3GraphFrame.configure(text='') 
        if self.heatmap03:
            self.heatmap03.get_tk_widget().destroy()
            self.heatmap03 = None
        ### delete BankRw0Cn2DbscanFrame
        self.BankRw0Cn2DbscanFrame.configure(text='')
        if self.dbsAllTree:
            self.dbsAllTree.destroy()
            self.dbsAllTree = None  
        ### delete countyOfRw2Cn3DbscanFrame
        self.countyOfRw2Cn3DbscanFrame.configure(text='')
        if self.dbsCountyTree:
            self.dbsCountyTree.destroy()
            self.dbsCountyTree = None            
        ### delete BankRw0Cn1DbscanFrame
        self.BankRw0Cn1DbscanFrame.configure(text='')
        if self.BankRw0Cn1RadiusDbscanFrame:
            self.BankRw0Cn1RadiusDbscanFrame.destroy()
            self.BankRw0Cn1RadiusDbscanFrame = None

        
        # Rw2
        # prcessing Tree: placeOfBank--------------------------------------------------------
        ### modify placeOfBankRw2Cn0Frame
        self.placeOfBankRw2Cn0Frame.configure(text=f'ATM同業策略 - 異業結盟 :「{self.selectedBank}」')       
        ### prcessing placeOfBankTree
        groupPlaceOfBank = dataSourceML.atmSelectedList(self.atmMLData,selectedBank=self.selectedBank,selectedItem='placetype')   
        self.groupPlaceOfBankList = groupPlaceOfBank.atmBankListOfItem()
        #print(self.groupPlaceOfBankList)        
        for item in self.placeOfBankTree.get_children():
            self.placeOfBankTree.delete(item)         
        for i in range(self.groupPlaceOfBankList['placetype'].size):
            self.placeOfBankTree.insert('', tk.END, 
                             values=[self.groupPlaceOfBankList.index[i]+1,self.groupPlaceOfBankList.iloc[i,0],self.groupPlaceOfBankList.iloc[i,1],self.groupPlaceOfBankList.iloc[i,2],self.groupPlaceOfBankList.iloc[i,3]],tags=self.groupPlaceOfBankList.iloc[i,0]
                            ) 
        self.placeOfBankTree.bind('<<TreeviewSelect>>',self.placeOfBankTreeSelected)  

        ### delete placeOfBankRw2Cn2GraphFrame     
        self.placeOfBankRw2Cn2GraphFrame.configure(text='')          
        if self.pie21:
            self.pie21.get_tk_widget().destroy()
            self.pie21 = None    
        ### delete placeOfBankRw2Cn1GraphFrame       
        self.placeOfBankRw2Cn1GraphFrame.configure(text='') 
        if self.scatter22:
            self.scatter22.get_tk_widget().destroy()
            self.scatter22 = None
             


    # Rw1(include:Rw0,Rw2) 
    def countyOfBankTreeSelected(self,event):      
        # prcessing Tree: countyOfBankRw1Cn0Frame--------------------------------
        selectedTree = event.widget 
        itemTage = selectedTree.selection()[0]      #selectedTree.selection()=('I005',)
        itemDic = selectedTree.item(itemTage)       #{'text': '', 'image': '', 'values': [812, '台新東高雄', ...], 'open': 0, 'tags': [5831]}
        self.selectedCounty = itemDic['tags'][0]
        #print(self.selectedCounty)          
        ### modify : configure
        self.countyOfBankRw1Cn0Frame.configure(text=f'ATM同業策略 - 區域佈局 :「{self.selectedBank} - {self.selectedCounty}」')  

        # prcessing pie: countyOfBankRw1Cn2GraphFrame--------------------------- 
        ### rank among competitiors
        self.atmSelectedCountyData = self.atmMLData[self.atmMLData['county']==self.selectedCounty]   #self.atmSelectedCountyData後面會用到
        rateCountOfBank = dataSourceML.atmRankAmongCompetitors(self.atmSelectedCountyData,selectedBank=self.selectedBank,rankNo=3)   
        self.rateBankOfCounty = rateCountOfBank.atmBankRateOfItem()
        #print(self.rateBankOfCounty)

        ### plot a graph in a labelframe using tkinter and matplotlib
        self.countyOfBankRw1Cn2GraphFrame.configure(text=f'絕對市占競爭「{self.selectedBank}-{self.selectedCounty}」') 
        if self.pie11:
            self.pie11.get_tk_widget().destroy()
            self.pie11 = None  
                
        fig11 = plt.Figure(figsize=(2,1.93), dpi=100)
        fig11.patch.set_facecolor('lightgrey')
        fig11.patch.set_alpha(0.3)
        ax11 = fig11.add_subplot(111)
        self.pie11 = FigureCanvasTkAgg(fig11, self.countyOfBankRw1Cn2GraphFrame)
        self.pie11.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        bankbrifname = self.rateBankOfCounty['bankbrifname']
        unitsCount = self.rateBankOfCounty['unitsCount']        
        explodes = [0 if x!=0 else 0.1 for x in range(self.rateBankOfCounty['bankbrifname'].size)]
        explodes = tuple(explodes)
        colors = ["lightblue","red","orange","yellow","lightgreen"]
        ax11.pie(unitsCount, labels=bankbrifname,colors=colors,explode=explodes,autopct="%2.0f%%",startangle=90,labeldistance=1.2,textprops={'fontsize': 8})

        
        # prcessing scatter: countyOfBankRw1Cn1GraphFrame--------------------------- 
        ### ScatterSize of District  
        self.atmSelectedCountyBankData = self.atmSelectedCountyData[self.atmSelectedCountyData['bankbrifname']==self.selectedBank] 
        scatterSizeDistOfCoutyBank = dataSourceML.atmScatterSizeOfDistrict(self.atmSelectedCountyBankData,grpBase='district')   
        self.scatterSizeDistOfCoutyBank = scatterSizeDistOfCoutyBank.atmScatterSize()
        #print(self.scatterSizeDistOfCoutyBank)
        distUnits = self.scatterSizeDistOfCoutyBank['unitsCount'].size

        ### plot a graph in a labelframe using tkinter and matplotlib
        self.countyOfBankRw1Cn1GraphFrame.configure(text=f'「{self.selectedBank}」於「{self.selectedCounty} {distUnits} 個行政區」設點') 
        if self.scatter12:
            self.scatter12.get_tk_widget().destroy()
            self.scatter12 = None        
        
        fig12 = plt.Figure(figsize=(3,1.93), dpi=100)
        fig12.patch.set_facecolor('lightgrey')
        fig12.patch.set_alpha(0.3)
        ax12 = fig12.add_subplot(111)
        ax12.patch.set_facecolor('lightyellow')
        self.scatter12 = FigureCanvasTkAgg(fig12, self.countyOfBankRw1Cn1GraphFrame)
        self.scatter12.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)    

        x = self.scatterSizeDistOfCoutyBank['lngOfDisCenter']
        y = self.scatterSizeDistOfCoutyBank['latOfDisCenter']
        sizes = self.scatterSizeDistOfCoutyBank['unitsCount']  
        colors=['darkred','red', 'mediumvioletred', 'blue']
        xtick =self.scatterSizeDistOfCoutyBank['district'].str[:2]+": "+self.scatterSizeDistOfCoutyBank['unitsCount'].astype(str)
        for i in range(self.scatterSizeDistOfCoutyBank['district'].size):
            if i < 3:
                ax12.scatter(x[i], y[i], color=colors[i], s=sizes[i], label=xtick[i])
            else:
                ax12.scatter(x[i], y[i], color=colors[3], s=sizes[i])
        ax12.legend(loc='best', fontsize=7)

        ax12.tick_params(axis='x',which='major',labelsize=7)
        ax12.tick_params(axis='x',which='minor',labelsize=5)
        ax12.tick_params(axis='y',which='major',labelsize=7)
        ### setting        
        xmajorLocator  = MultipleLocator(0.1)          # x轴刻度间隔 0.1
        xminorLocator  = MultipleLocator(0.05)         # x轴刻度间隔 0.05
        ymajorLocator  = MultipleLocator(0.05)         # y轴刻度间隔 0.05                 
        ax12.xaxis.set_major_locator(xmajorLocator)    
        ax12.xaxis.set_minor_locator(xminorLocator) 
        ax12.yaxis.set_major_locator(ymajorLocator)            
        ax12.grid(color = "grey", alpha = 0.25)
        ax12.set_axisbelow(True)  
        fig12.subplots_adjust(top=0.985,left=0.13,bottom=0.12,right=0.97,hspace=0.2,wspace=0.2)
         
        # prcessing Dbscan: BankRw0Cn1DbscanFrame------------------------------------
        # prcessing Dbscan: BankRw0Cn2DbscanFrame,BankRw0Cn3GraphFrame---------------
        # prcessing Dbscan: countyOfBankRw1Cn3GraphFrame,countyOfRw2Cn3DbscanFrame---
        ### delete BankRw0Cn3GraphFrame     
        self.BankRw0Cn3GraphFrame.configure(text='') 
        if self.heatmap03:
            self.heatmap03.get_tk_widget().destroy()
            self.heatmap03 = None
        ### delete BankRw0Cn2DbscanFrame
        self.BankRw0Cn2DbscanFrame.configure(text='')
        if self.dbsAllTree:
            self.dbsAllTree.destroy()
            self.dbsAllTree = None            
        ### delete countyOfBankRw1Cn3GraphFrame       
        self.countyOfBankRw1Cn3GraphFrame.configure(text='') 
        if self.heatmap13:
            self.heatmap13.get_tk_widget().destroy()
            self.heatmap13 = None
        ### delete countyOfRw2Cn3DbscanFrame
        self.countyOfRw2Cn3DbscanFrame.configure(text='')
        if self.dbsCountyTree:
            self.dbsCountyTree.destroy()
            self.dbsCountyTree = None           
        ### delete BankRw0Cn1DbscanFrame
        if self.BankRw0Cn1RadiusDbscanFrame:
            self.BankRw0Cn1RadiusDbscanFrame.destroy()
            self.BankRw0Cn1RadiusDbscanFrame = None
        
        self.BankRw0Cn1DbscanFrame.configure(text='相對距離競爭 - DBSCAN密度半徑(eps)參數設定')
        self.BankRw0Cn1RadiusDbscanFrame = ttk.Frame(self.BankRw0Cn1DbscanFrame)
        self.BankRw0Cn1RadiusDbscanFrame.grid(row=0, column=0, sticky=tk.W) 
           
        # processing DBSCANdata: ------------------------
        # default: stdType = 'maxStd' ; stdRatio = 1/55
        # default: stdType = 'minStd' ; stdRatio = 1/45
        self.stdTypeVar = tk.StringVar()
        self.stdQ25Var = tk.StringVar() 
        self.stdRatioVar = tk.StringVar() 
        self.stdTypeVar.set('max')
        self.stdQ25Var.set('Y')
        self.stdRatioVar.set(55)

        self.stdTypeLabelMax = ttk.Label(self.BankRw0Cn1RadiusDbscanFrame,text="step1: max(經度Std, 緯度Std), 輸入max") 
        self.stdTypeLabelMax.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(7,0)) 
        self.stdTypeLabelMin = ttk.Label(self.BankRw0Cn1RadiusDbscanFrame,text="min (經度Std, 緯度Std), 輸入min")
        self.stdTypeLabelMin.grid(row=1, column=0, sticky=tk.W, padx=(48,10), pady=(1,5))
        self.stdTypeEntry = ttk.Entry(self.BankRw0Cn1RadiusDbscanFrame, textvariable=self.stdTypeVar, justify='center', width=5)
        self.stdTypeEntry.grid(row=0, column=1, sticky=tk.E, rowspan=2, padx=(2,12), pady=7, ipady=5)  
        #第25 百分位數
        #self.stdQ25Label = ttk.Label(self.BankRw0Cn1RadiusDbscanFrame,text="step2: 上述Std>=25th percentile, 輸入Y")   
        #第1 四分位數
        self.stdQ25Label = ttk.Label(self.BankRw0Cn1RadiusDbscanFrame,text="step2: 上述Std>=first quartile,Q1, 輸入Y")   
        self.stdQ25Label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=(7,0)) 
        self.stdQ25Entry = ttk.Entry(self.BankRw0Cn1RadiusDbscanFrame, textvariable=self.stdQ25Var, justify='center', width=5)
        self.stdQ25Entry.grid(row=2, column=1, sticky=tk.E, padx=(2,12), pady=7, ipady=1) 
            
        self.stdRatioLabelMax = ttk.Label(self.BankRw0Cn1RadiusDbscanFrame,text="step3: max(經緯度Std) * (1/55), 輸入55")
        self.stdRatioLabelMax.grid(row=3, column=0, sticky=tk.W, padx=10, pady=(7,0))  
        self.stdRatioLabelMin = ttk.Label(self.BankRw0Cn1RadiusDbscanFrame,text="min (經緯度Std) * (1/45), 輸入45")
        self.stdRatioLabelMin.grid(row=4, column=0, sticky=tk.W, padx=(48,10), pady=(1,5))
        self.stdRatioEntry = ttk.Entry(self.BankRw0Cn1RadiusDbscanFrame, textvariable=self.stdRatioVar, justify='center', width=5)
        self.stdRatioEntry.grid(row=3, column=1, sticky=tk.E, rowspan=2, padx=(2,12), pady=7, ipady=5)

        self.comitButton=ttk.Button(self.BankRw0Cn1RadiusDbscanFrame,text="確認",command=self.countyOfBankClusterDBSCAN, width=38)
        self.comitButton.grid(row=5, column=0, columnspan=2, sticky=tk.E, padx=(10,12), pady=(19,10))

        
    def countyOfBankClusterDBSCAN(self):     
        self.stdTypeValue = self.stdTypeVar.get()   
        self.stdTypeValue = self.stdTypeValue.lower() + 'Std'   
        #self.stdRatioValue = self.stdRatioVar.get()
        self.stdRatioValue = float(self.stdRatioVar.get())
        self.stdRatioValue = 1/self.stdRatioValue
        self.stdQ25Value = self.stdQ25Var.get().upper()
        #print(self.stdTypeValue, self.stdRatioValue, self.stdQ25Value)
        atmClusterData = dataSourceML.atmSklearnCluster(self.atmMLData, stdType = self.stdTypeValue, stdRatio = self.stdRatioValue, stdQ25 = self.stdQ25Value)
        self.clusterTeamDBSCAN,self.clusterRadiusDBSCAN = atmClusterData.atmClusterDBSCAN()    
        
    
        # prcessing heatmap: countyOfBankRw1Cn3GraphFrame---------------------------         
        ###clusterTeamDBSCAN, clusterRadiusDBSCAN
        corrBankDBSCAN = self.clusterTeamDBSCAN[ (self.clusterTeamDBSCAN['dbscan組'] != -1) & (self.clusterTeamDBSCAN['縣市'] == self.selectedCounty ) ]        
        corrBankDBSCAN = corrBankDBSCAN[['一銀','中信','元大','兆豐','台新','合庫','國世','土銀','彰銀','永豐','玉山','臺企','臺銀','華銀','郵局']]
        ### plot a graph in a labelframe using tkinter and matplotlib
        self.countyOfBankRw1Cn3GraphFrame.configure(text=f'相對距離競爭-「{self.selectedCounty}」同業設點「相關性」') 
        if self.heatmap13:
            self.heatmap13.get_tk_widget().destroy()
            self.heatmap13 = None    

        fig13 = plt.Figure(figsize=(3.45,1.93), dpi=100)
        fig13.patch.set_facecolor('lightgrey')
        fig13.patch.set_alpha(0.3)
        ax13 = fig13.add_subplot(111)
        self.heatmap13 = FigureCanvasTkAgg(fig13, self.countyOfBankRw1Cn3GraphFrame)
        self.heatmap13.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)   

        corrBank = corrBankDBSCAN.corr()
        ax13 = sns.heatmap (corrBank, ax=ax13, cmap="Blues", xticklabels=corrBankDBSCAN.columns, yticklabels=corrBankDBSCAN.columns,
                            cbar=False, annot=True, fmt='.1f', annot_kws={"size": 6})
        ax13.set_yticklabels(corrBankDBSCAN.columns, size = 7.5)
        ax13.set_xticklabels(corrBankDBSCAN.columns, size = 7)
        fig13.subplots_adjust(top=0.985,left=0.11,bottom=0.18,right=0.97,hspace=0.2,wspace=0.2)

        
        # Rw0:全台---------------------------------------------------------------------------------         
        # prcessing heatmap: BankRw0Cn3GraphFrame-----------------------------------  
        # clusterTeamDBSCAN, clusterRadiusDBSCAN
        corrBankDBSCAN = self.clusterTeamDBSCAN[ self.clusterTeamDBSCAN['dbscan組'] != -1 ]        
        corrBankDBSCAN = corrBankDBSCAN[['一銀','中信','元大','兆豐','台新','合庫','國世','土銀','彰銀','永豐','玉山','臺企','臺銀','華銀','郵局']]
        ### plot a graph in a labelframe using tkinter and matplotlib
        self.BankRw0Cn3GraphFrame.configure(text='相對距離競爭-「全台」同業設點「相關性」') 
        if self.heatmap03:
            self.heatmap03.get_tk_widget().destroy()
            self.heatmap03 = None    

        fig03 = plt.Figure(figsize=(3.45,1.93), dpi=100)
        fig03.patch.set_facecolor('lightgrey')
        fig03.patch.set_alpha(0.3)
        ax03 = fig03.add_subplot(111)
        self.heatmap03 = FigureCanvasTkAgg(fig03, self.BankRw0Cn3GraphFrame)
        self.heatmap03.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH) 

        corrBank = corrBankDBSCAN.corr()
        #Purples,greys,OrRd
        ax03 = sns.heatmap (corrBank, ax=ax03, cmap="OrRd", xticklabels=corrBankDBSCAN.columns, yticklabels=corrBankDBSCAN.columns,
                            cbar=False, annot=True, fmt='.1f', annot_kws={"size": 6})
        ax03.set_yticklabels(corrBankDBSCAN.columns, size = 7.5)
        ax03.set_xticklabels(corrBankDBSCAN.columns, size = 7)
        fig03.subplots_adjust(top=0.985,left=0.11,bottom=0.18,right=0.97,hspace=0.2,wspace=0.2)                


        ## BankRw0Cn2DbscanFrame, DbscanTree ----------------------------
        clusterTeamData = self.clusterTeamDBSCAN
        clusterTeamCnt = dataSourceML.atmClusterCntTypeDBSCAN(clusterTeamData)
        clusterCntTypeDBSCAN = clusterTeamCnt.atmClusterCntType()
        #print(clusterCntTypeDBSCAN) 
        
        self.BankRw0Cn2DbscanFrame.configure(text='「全台」DBSCAN分組說明: ')
        if self.dbsAllTree:
            self.dbsAllTree.destroy()
            self.dbsAllTree = None      

        # build ttk.Treeview
        columns = ('#1', '#2', '#3', '#4')
        self.dbsAllTree = ttk.Treeview(self.BankRw0Cn2DbscanFrame, columns=columns, show='headings', height=8)
        ### define headings
        self.dbsAllTree.heading('#1', text='據點數別')
        self.dbsAllTree.column('#1', minwidth=0, width=60, anchor='e')
        self.dbsAllTree.heading('#2', text='筆數')
        self.dbsAllTree.column('#2', minwidth=0, width=41, anchor='e')
        self.dbsAllTree.heading('#3', text='設點數')
        self.dbsAllTree.column('#3', minwidth=0, width=45, anchor="e") 
        self.dbsAllTree.heading('#4', text='比率')
        self.dbsAllTree.column('#4', minwidth=0, width=41, anchor="e") 
        self.dbsAllTree.pack(side=tk.RIGHT,padx=5,pady=(2,4)) 

        ### delete and add
        for item in self.dbsAllTree.get_children():
            self.dbsAllTree.delete(item)         
        for i in range(clusterCntTypeDBSCAN['dbs據點數別'].size):
            self.dbsAllTree.insert('', tk.END, 
                             values=[clusterCntTypeDBSCAN.iloc[i,0],clusterCntTypeDBSCAN.iloc[i,1],clusterCntTypeDBSCAN.iloc[i,2],clusterCntTypeDBSCAN.iloc[i,3]])


        # Rw2:各縣市---------------------------------------------------------------------------------
        ## countyOfRw2Cn3DbscanFrame, DbscanTree ----------------------------         
        countyOfClusterTeamData = self.clusterTeamDBSCAN[self.clusterTeamDBSCAN['縣市']==self.selectedCounty ]        
        countyOfClusterTeamCnt = dataSourceML.atmClusterCntTypeDBSCAN(countyOfClusterTeamData)
        countyOfClusterCntTypeDBSCAN = countyOfClusterTeamCnt.atmClusterCntType()
        #print(countyOfClusterCntTypeDBSCAN)        
        
        self.countyOfRw2Cn3DbscanFrame.configure(text=f'「{self.selectedCounty}」DBSCAN分組說明: ')
        if self.dbsCountyTree:
            self.dbsCountyTree.destroy()
            self.dbsCountyTree = None

        # build ttk.Treeview
        columns = ('#1', '#2', '#3', '#4')
        self.dbsCountyTree = ttk.Treeview(self.countyOfRw2Cn3DbscanFrame, columns=columns, show='headings', height=8)
        ### define headings
        self.dbsCountyTree.heading('#1', text='據點數別')
        self.dbsCountyTree.column('#1', minwidth=0, width=60, anchor='e')
        self.dbsCountyTree.heading('#2', text='筆數')
        self.dbsCountyTree.column('#2', minwidth=0, width=41, anchor='e')
        self.dbsCountyTree.heading('#3', text='設點數')
        self.dbsCountyTree.column('#3', minwidth=0, width=45, anchor="e") 
        self.dbsCountyTree.heading('#4', text='比率')
        self.dbsCountyTree.column('#4', minwidth=0, width=41, anchor="e") 
        self.dbsCountyTree.pack(side=tk.RIGHT,padx=5,pady=(2,4))  
        
        ### delete and add
        for item in self.dbsCountyTree.get_children():
            self.dbsCountyTree.delete(item)         
        for i in range(countyOfClusterCntTypeDBSCAN['dbs據點數別'].size):
            self.dbsCountyTree.insert('', tk.END, 
                             values=[countyOfClusterCntTypeDBSCAN.iloc[i,0],countyOfClusterCntTypeDBSCAN.iloc[i,1],countyOfClusterCntTypeDBSCAN.iloc[i,2],countyOfClusterCntTypeDBSCAN.iloc[i,3]])





    # Rw2 
    def placeOfBankTreeSelected(self,event):    
        # prcessing Tree: placeOfBankRw2Cn0Frame--------------------------------     
        selectedTree = event.widget 
        itemTage = selectedTree.selection()[0]      #selectedTree.selection()=('I005',)
        itemDic = selectedTree.item(itemTage)       #{'text': '', 'image': '', 'values': [812, '台新東高雄', ...], 'open': 0, 'tags': [5831]}
        self.selectedPlace = itemDic['tags'][0]
        #print(self.selectedPlace) 
        ### modify configure
        self.placeOfBankRw2Cn0Frame.configure(text=f'ATM同業策略 - 異業結盟 :「{self.selectedBank} - {self.selectedPlace}」')

        # prcessing pie: placeOfBankRw2Cn2GraphFrame--------------------------- 
        ### rank among competitiors
        self.atmSelectedPlaceData = self.atmMLData[self.atmMLData['placetype']==self.selectedPlace]
        ratePlaceOfBank = dataSourceML.atmRankAmongCompetitors(self.atmSelectedPlaceData,selectedBank=self.selectedBank,rankNo=3)   
        self.rateBankOfPlace = ratePlaceOfBank.atmBankRateOfItem()
        #print(self.rateBankOfPlace)

        ### plot a graph in a labelframe using tkinter and matplotlib
        self.placeOfBankRw2Cn2GraphFrame.configure(text=f'絕對市占競爭「{self.selectedBank}-{self.selectedPlace}」')    
        if self.pie21:
            self.pie21.get_tk_widget().destroy()
            self.pie21 = None

        fig21 = plt.Figure(figsize=(2,1.93), dpi=100)
        fig21.patch.set_facecolor('lightgrey')
        fig21.patch.set_alpha(0.3)
        ax21 = fig21.add_subplot(111)
        self.pie21 = FigureCanvasTkAgg(fig21, self.placeOfBankRw2Cn2GraphFrame)
        self.pie21.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        bankbrifname = self.rateBankOfPlace['bankbrifname']
        unitsCount = self.rateBankOfPlace['unitsCount']
        explodes = [0 if x!=0 else 0.1 for x in range(self.rateBankOfPlace['bankbrifname'].size)]
        explodes = tuple(explodes)
        colors = ["lightblue","red","orange","yellow","lightgreen"]
        ax21.pie(unitsCount, labels=bankbrifname,colors=colors,explode=explodes,autopct="%2.0f%%",startangle=90,labeldistance=1.2,textprops={'fontsize': 8})  
        
        
        # prcessing scatter: placeOfBankRw2Cn1GraphFrame--------------------------- 
        ### ScatterSize of County  
        self.atmSelectedPlaceBankData = self.atmSelectedPlaceData[self.atmSelectedPlaceData['bankbrifname']==self.selectedBank]         
        scatterSizeCouOfPlaceBank = dataSourceML.atmScatterSizeOfDistrict(self.atmSelectedPlaceBankData,grpBase='county')   
        self.scatterSizeCouOfPlaceBank = scatterSizeCouOfPlaceBank.atmScatterSize()
        #print(self.scatterSizeCouOfPlaceBank)
        placeUnits = self.scatterSizeCouOfPlaceBank['unitsCount'].size

        ### plot a graph in a labelframe using tkinter and matplotlib
        self.placeOfBankRw2Cn1GraphFrame.configure(text=f'「{self.selectedBank}- {self.selectedPlace}」於「{placeUnits} 個縣市」設點') 
        if self.scatter22:
            self.scatter22.get_tk_widget().destroy()
            self.scatter22 = None        
        
        fig22 = plt.Figure(figsize=(3,1.93), dpi=100)
        fig22.patch.set_facecolor('lightgrey')
        fig22.patch.set_alpha(0.3)
        ax22 = fig22.add_subplot(111)
        ax22.patch.set_facecolor('lightyellow')    
        self.scatter22 = FigureCanvasTkAgg(fig22, self.placeOfBankRw2Cn1GraphFrame)
        self.scatter22.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)      

        x = self.scatterSizeCouOfPlaceBank['lngOfCouCenter']
        y = self.scatterSizeCouOfPlaceBank['latOfCouCenter']
        sizes = self.scatterSizeCouOfPlaceBank['unitsCount']
        #label -----
        colors=['darkred','red', 'mediumvioletred', 'blue']
        xtick =self.scatterSizeCouOfPlaceBank['county'].str[:2]+": "+self.scatterSizeCouOfPlaceBank['unitsCount'].astype(str)
        for i in range(self.scatterSizeCouOfPlaceBank['county'].size):
            if i < 3:
                ax22.scatter(x[i], y[i], color=colors[i], s=sizes[i], label=xtick[i])
            else:
                ax22.scatter(x[i], y[i], color=colors[3], s=sizes[i])
        ax22.legend(loc='best', fontsize=7)
        #ax22.legend(loc='best', numpoints=1, ncol=3, fontsize=7)
        ax22.tick_params(axis='x',which='major',labelsize=7)
        ax22.tick_params(axis='x',which='minor',labelsize=5)
        ax22.tick_params(axis='y',which='major',labelsize=7) 
        #setting        
        xmajorLocator  = MultipleLocator(0.5)         # x轴刻度间隔 0.1
        xminorLocator  = MultipleLocator(0.25)        # x轴刻度间隔 0.05
        ymajorLocator  = MultipleLocator(0.5)         # y轴刻度间隔 0.05                 
        ax22.xaxis.set_major_locator(xmajorLocator)    
        ax22.xaxis.set_minor_locator(xminorLocator) 
        ax22.yaxis.set_major_locator(ymajorLocator)            
        ax22.grid(color = "grey", alpha = 0.2)
        ax22.set_axisbelow(True)          
        fig22.subplots_adjust(top=0.985,left=0.13,bottom=0.12,right=0.97,hspace=0.2,wspace=0.2)






def main():
    
    # get atmData from internet----------------------   
    dataSource.DownLoadAtmData()    
    
    
    # preprocess data--------------------------------
    atmData = pd.read_csv('atmData.csv')
    atmMLData = dataSourceML.preprocessingOfBankName(atmData)
    #print(atmMLData.info())
    
    # build window()-------------------------------
    window = Window(atmMLData)
    window.title("ATM裝設地點: 同業競爭及策略分析")
    window.geometry("1270x660")
    window.mainloop()
    
    
    

    


if __name__=="__main__":
    main()