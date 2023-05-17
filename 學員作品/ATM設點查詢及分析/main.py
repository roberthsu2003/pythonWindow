import dataSource
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
import tkintermapview as tkmap     #pip install tkintermapview


radiusStart = 100
radiusEnd = 1000

class Window(tk.Tk):
    def __init__(self,atmData):
        super().__init__()
        self.atmData = atmData
        
        # Mainframe:-------------------------------------------------------------------
        mainFrame = ttk.Frame(self)
        mainFrame.pack(fill=tk.X,padx=10,pady=10)

        # ATM地點 : 查詢輸入 - --------------------------------------------
        self.filterTopLeftFrame = ttk.LabelFrame(mainFrame,text='ATM地點 : 查詢輸入')
        self.filterTopLeftFrame.grid(column=0, row=0, padx=10, pady=5)

        ## row=0:縣市別----
        ttk.Label(self.filterTopLeftFrame, text = "請選擇-縣市 :", font = ("Arial", 10)).grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
        self.countyComBox = ttk.Combobox(self.filterTopLeftFrame,state='readonly',width=20)
        self.countyComBox.grid(column=1, row=0, pady=5, sticky=tk.W, columnspan=2)        
             
        countyList = self.atmData['county'].unique().tolist()          #unique->numpy.ndarray, tolist->list
        countyList = sorted(countyList)
        countyList.insert(0,'請選擇---')
        self.countyComboxValues = tuple(countyList)
        self.countyComBox['values'] = self.countyComboxValues
        self.countyComBox.current(0)
        self.countyComBox.bind('<<ComboboxSelected>>',self.countyChangeEventCombox)

        ## row=1:區鄕鎮縣市----
        ttk.Label(self.filterTopLeftFrame, text = "請選擇-區鄕鎮縣市 :", font = ("Arial", 10)).grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
        self.districtComBox = ttk.Combobox(self.filterTopLeftFrame,state='readonly',width=20)
        self.districtComBox.grid(column=1, row=1, padx=(0,10), pady=5, sticky=tk.W, columnspan=2)        
        self.districtComBox['values'] = ('請選擇---')
        self.districtComBox.current(0)

        ## row=2:地址----
        ttk.Label(self.filterTopLeftFrame, text = "請輸入-地址 :", font = ("Arial", 10)).grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)  
        self.addressStringVarButton = tk.StringVar()
        addressEntry = ttk.Entry(self.filterTopLeftFrame, textvariable=self.addressStringVarButton, font = ("Arial", 10), width= 22)
        addressEntry.grid(column=1, row=2, padx=(0,10), pady=5, sticky=tk.W, columnspan=2)
        
        ## row=3, row=4:距離半徑----
        ttk.Label(self.filterTopLeftFrame, text = "請確認-周圍半徑 :", font = ("Arial", 10)).grid(column=0, row=3, padx=10, pady=8,sticky=tk.W) 
        self.radiusIntVarScale = tk.IntVar()
        self.radiusIntVarScale.set(radiusStart)
        self.radiusScale = ttk.Scale(self.filterTopLeftFrame, orient=tk.HORIZONTAL, length=160, from_=radiusStart, to=radiusEnd, variable=self.radiusIntVarScale,command=self.radiusChangeEventScale)                 
        self.radiusScale.grid(column=1, row=3, padx=(0,10), pady=(5,0), sticky=tk.W, columnspan=2)

        ttk.Label(self.filterTopLeftFrame, text = "半徑(公尺) :", font = ("Arial", 9)).grid(column=1, row=4, sticky=tk.W) 
        self.radiusLabel = ttk.Label(self.filterTopLeftFrame, text = self.radiusIntVarScale.get(), font = ("Arial", 9))
        self.radiusLabel.grid(column=2, row=4, padx=(0,15), sticky=tk.E)

        ## row=5:confirm or clear----
        addressConfirmButton=ttk.Button(self.filterTopLeftFrame,text="確認",width=4,command=self.confirmEventButton)
        addressConfirmButton.grid(column=1, row=5, padx=(0,3), pady=(5,5), sticky=tk.W, ipadx=14, ipady=2)

        addressClearButton=ttk.Button(self.filterTopLeftFrame,text="清除",width=4,command=self.clearEventButton)
        addressClearButton.grid(column=2, row=5, padx=(0,15), pady=(5,5), sticky=tk.E, ipadx=14, ipady=2)


        # ATM地點 : 彙總摘要--------------------------------------------       
        self.resultBriefMiddleLeftFrame = ttk.LabelFrame(mainFrame,text='ATM地點 : 彙總摘要')
        self.resultBriefMiddleLeftFrame.grid(column=0, row=1, padx=10, pady=5, rowspan=2)
        
        ## row=0:半徑內的ATM總台數----
        ttk.Label(self.resultBriefMiddleLeftFrame, text = "距半徑內的ATM總台數 :", font = ("Arial", 10)).grid(column=0, row=0, padx=(10,75), pady=3,sticky=tk.W)
        self.unitTotalText = tk.Text(self.resultBriefMiddleLeftFrame,height=1,width=10,state=tk.DISABLED) 
        self.unitTotalText.grid(column=1, row=0, sticky=tk.E, padx=(0,10), pady=3)
        
        ## row=1:金融機構(含郵局)家數----
        ttk.Label(self.resultBriefMiddleLeftFrame, text = "金融機構(含郵局) 家數 :", font = ("Arial", 10)).grid(column=0, row=1, padx=(10,75), pady=3,sticky=tk.W)
        self.branchTotalText = tk.Text(self.resultBriefMiddleLeftFrame,height=1,width=10,state=tk.DISABLED) 
        self.branchTotalText.grid(column=1, row=1, sticky=tk.E, padx=(0,10), pady=3)

        ## row=2:地點類別總數----
        ttk.Label(self.resultBriefMiddleLeftFrame, text = "裝設地點類別的總個數 :", font = ("Arial", 10)).grid(column=0, row=2, padx=(10,75), pady=3,sticky=tk.W)
        self.placeTotalText = tk.Text(self.resultBriefMiddleLeftFrame,height=1,width=10,state=tk.DISABLED) 
        self.placeTotalText.grid(column=1, row=2, sticky=tk.E, padx=(0,10), pady=3)
        
        ## row=3:無障空間區(輪椅)總台數----
        ttk.Label(self.resultBriefMiddleLeftFrame, text = "無障礙區(輪椅) 據點數 :", font = ("Arial", 10)).grid(column=0, row=3, padx=(10,75), pady=3,sticky=tk.W)
        self.wheelTotalText = tk.Text(self.resultBriefMiddleLeftFrame,height=1,width=10,state=tk.DISABLED) 
        self.wheelTotalText.grid(column=1, row=3, sticky=tk.E, padx=(0,10), pady=3)
        
        ## row=4:無障空間區(語音)總台數----
        ttk.Label(self.resultBriefMiddleLeftFrame, text = "無障礙區(語音) 據點數 :", font = ("Arial", 10)).grid(column=0, row=4, padx=(10,75), pady=3,sticky=tk.W)
        self.voiceTotalText = tk.Text(self.resultBriefMiddleLeftFrame,height=1,width=10,state=tk.DISABLED) 
        self.voiceTotalText.grid(column=1, row=4, sticky=tk.E, padx=(0,10), pady=3)
        
        # ATM地點 : 地圖標示--------------------------------------------
        self.resultMapTopRightFrame = ttk.LabelFrame(mainFrame,text='ATM地點 : 地圖標示')
        self.resultMapTopRightFrame.grid(column=1,row=0,padx=10,pady=5, rowspan=2)

        self.resultTkinterMapView = tkmap.TkinterMapView(self.resultMapTopRightFrame,width=864,height=327,corner_radius=0)
        self.resultTkinterMapView.pack(side=tk.LEFT,padx=10, pady=10)

        # 預設職能上課地點 :台北市大安區信義路三段153號
        self.markerNow = self.resultTkinterMapView.set_position(25.03380218, 121.54039791500624, text_color = 'darkRed', marker=True)        
        self.resultTkinterMapView.set_zoom(20) 
        #self.markerNow.set_text('職能管理發展學院-大安區')     


        # ATM地點 : 明細結果--------------------------------------------
        self.resultDetailBottomFrame = ttk.LabelFrame(self,text='ATM地點 : 明細清單')     #self.addressSelectValue+self.districtSelectValue
        self.resultDetailBottomFrame.pack(side=tk.LEFT,padx=(20,10),pady=(0,10))
        # build ttk.Treeview
        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10', '#11', '#12', '#13')
        self.tree = ttk.Treeview(self.resultDetailBottomFrame, columns=columns, show='headings')
        ### define headings
        self.tree.heading('#1', text='銀行代號')
        self.tree.column('#1', minwidth=0, width=60)
        self.tree.heading('#2', text='銀行簡稱')
        self.tree.column('#2', minwidth=0, width=82)
        self.tree.heading('#3', text='裝設型態')
        self.tree.column('#3', minwidth=0, width=60)
        self.tree.heading('#4', text='裝設地點類別')
        self.tree.column('#4', minwidth=0, width=120)
        self.tree.heading('#5', text='裝設地點')
        self.tree.column('#5', minwidth=0, width=180)
        self.tree.heading('#6', text='縣市')
        self.tree.column('#6', minwidth=0, width=60)   
        self.tree.heading('#7', text='鄉鎮縣市')
        self.tree.column('#7', minwidth=0, width=75)    
        self.tree.heading('#8', text='地址')
        self.tree.column('#8', minwidth=0, width=220)  
        self.tree.heading('#9', text='輪椅')
        self.tree.column('#9', minwidth=0, width=34)   
        self.tree.heading('#10', text='語音')
        self.tree.column('#10', minwidth=0, width=34)   
        self.tree.heading('#11', text='台數')
        self.tree.column('#11', minwidth=0, width=34)   
        self.tree.heading('#12', text='距離(M)')
        self.tree.column('#12', minwidth=0, width=60)
        self.tree.heading('#13', text='備註')
        self.tree.column('#13', minwidth=0, width=170)      
        self.tree.pack(side=tk.LEFT,padx=10,pady=(0,10))

        ### build ttk.scrollBar
        scrollBar = ttk.Scrollbar(self.resultDetailBottomFrame,orient='vertical',command=self.tree.yview)
        scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollBar.set)
        


    # FUNCTIONS -------------------------------------------------------------------------------------------------------------------------
    def countyChangeEventCombox(self,event):
        countyEvent = event.widget
        countySelect = countyEvent.current()
        self.countySelectValue = self.countyComboxValues[countySelect]        
        #print(self.countySelectValue)

        # row=1:區鄕鎮縣市 ------
        self.districtUnderCounty = self.atmData[self.atmData['county'] == self.countySelectValue]
        districtList = self.districtUnderCounty['district'].unique().tolist()    #unique->numpy.ndarray,tolist->list 
        districtList = sorted(districtList)
        districtList.insert(0,'請選擇---')
        self.districtComboxValues = tuple(districtList)
        self.districtComBox['values'] = self.districtComboxValues
        self.districtComBox.current(0)
        self.districtComBox.bind('<<ComboboxSelected>>',self.districtChangeEventCombox)        

    def districtChangeEventCombox(self,event):
        districtEvent = event.widget
        districtSelect = districtEvent.current()
        self.districtSelectValue = self.districtComboxValues[districtSelect]
        #print(self.districtSelectValue)    
    
    def radiusChangeEventScale(self,event):         
        self.radiusSelectValue = self.radiusIntVarScale.get()   # or = self.radiusScale.get()
        self.radiusLabel.configure(text = self.radiusSelectValue)
        #print(self.radiusSelectValue) 
    
    def clearEventButton(self):
        # clear filterTopLeftFrame-----------------------------
        self.countyComBox.current(0) 
        self.districtComBox.current(0)
        self.addressStringVarButton.set('')
        self.radiusIntVarScale.set(radiusStart)
        self.radiusLabel.configure(text = self.radiusIntVarScale.get())
        for item in self.tree.get_children():
            self.tree.delete(item) 

        # clear resultBriefMiddleLeftFrame----------------------
        self.unitTotalText.configure(state=tk.NORMAL)
        self.branchTotalText.configure(state=tk.NORMAL)
        self.placeTotalText.configure(state=tk.NORMAL)
        self.wheelTotalText.configure(state=tk.NORMAL)
        self.voiceTotalText.configure(state=tk.NORMAL)
        self.unitTotalText.delete('1.0',tk.END)
        self.branchTotalText.delete('1.0',tk.END)
        self.placeTotalText.delete('1.0',tk.END)
        self.wheelTotalText.delete('1.0',tk.END)
        self.voiceTotalText.delete('1.0',tk.END)
        self.unitTotalText.configure(state=tk.DISABLED)
        self.branchTotalText.configure(state=tk.DISABLED)
        self.placeTotalText.configure(state=tk.DISABLED)
        self.wheelTotalText.configure(state=tk.DISABLED)
        self.voiceTotalText.configure(state=tk.DISABLED) 

        # clear resultDetailBottomFrame-------------------------
        self.resultDetailBottomFrame.configure(text=f'ATM地點 : 明細清單 : ')

        # clear resultMapTopRightFrame-------------------------
        self.resultTkinterMapView.delete_all_marker()
        # 預設職能上課地點 :台北市大安區信義路三段153號
        self.markerNow = self.resultTkinterMapView.set_position(25.03380218, 121.54039791500624, text_color = 'darkRed', marker=True)
        #self.markerNow.set_text('職能管理發展學院-大安區')


    def confirmEventButton(self):  
        # clear tree
        for item in self.tree.get_children():
            self.tree.delete(item) 

        # clear resultBriefMiddleLeftFrame----------------------
        self.unitTotalText.configure(state=tk.NORMAL)
        self.branchTotalText.configure(state=tk.NORMAL)
        self.placeTotalText.configure(state=tk.NORMAL)
        self.wheelTotalText.configure(state=tk.NORMAL)
        self.voiceTotalText.configure(state=tk.NORMAL)
        self.unitTotalText.delete('1.0',tk.END)
        self.branchTotalText.delete('1.0',tk.END)
        self.placeTotalText.delete('1.0',tk.END)
        self.wheelTotalText.delete('1.0',tk.END)
        self.voiceTotalText.delete('1.0',tk.END)
        self.unitTotalText.configure(state=tk.DISABLED)
        self.branchTotalText.configure(state=tk.DISABLED)
        self.placeTotalText.configure(state=tk.DISABLED)
        self.wheelTotalText.configure(state=tk.DISABLED)
        self.voiceTotalText.configure(state=tk.DISABLED) 

        # get data 
        self.addressSelectValue = self.addressStringVarButton.get()  
        #print(self.addressSelectValue)   
        try:
            self.radiusSelectValue = self.radiusSelectValue
        except:
            self.radiusSelectValue = radiusStart

        # do filterAtmListFromInquiry of dataSource
        inquiryAddress = self.countySelectValue+self.districtSelectValue+self.addressSelectValue
        inquiryAtmList = dataSource.filterAtmListFromInquiry(inquiryAddress,self.radiusSelectValue,self.atmData)
        self.filterAtmList, self.longitude, self.latitude = inquiryAtmList.getDistanceBetweenPoints()
        
        # insert data to Text of resultBriefMiddleLeftFrame
        self.unitTotalText.configure(state=tk.NORMAL)
        self.branchTotalText.configure(state=tk.NORMAL)
        self.placeTotalText.configure(state=tk.NORMAL)
        self.wheelTotalText.configure(state=tk.NORMAL)
        self.voiceTotalText.configure(state=tk.NORMAL)
        self.unitTotalText.insert('insert',self.filterAtmList['units'].sum())
        self.branchTotalText.insert('insert',self.filterAtmList['bankcode'].unique().size)
        self.placeTotalText.insert('insert',self.filterAtmList['placetype'].unique().size)
        wheelTotalVar = self.filterAtmList['wheelchair_envir'].value_counts()
        voiceTotalVar = self.filterAtmList['voice_evnir'].value_counts()
        try:
            wheelTotalVar = wheelTotalVar['V']
        except:
            wheelTotalVar = 0
        try:
            voiceTotalVar = voiceTotalVar['V']
        except:
            voiceTotalVar = 0
        self.wheelTotalText.insert('insert',wheelTotalVar)  
        self.voiceTotalText.insert('insert',voiceTotalVar)
        self.unitTotalText.configure(state=tk.DISABLED)
        self.branchTotalText.configure(state=tk.DISABLED)
        self.placeTotalText.configure(state=tk.DISABLED)
        self.wheelTotalText.configure(state=tk.DISABLED)
        self.voiceTotalText.configure(state=tk.DISABLED) 

        # insert data to Treeview in resultDetailBottomFrame
        filterAtmListSize = self.filterAtmList['bankcode'].size
        self.resultDetailBottomFrame.configure(text=f'ATM地點 : 明細清單 : 共計 {filterAtmListSize} 筆')

        for i in range(self.filterAtmList['bankcode'].size):
            self.tree.insert('', tk.END, 
                             values=[self.filterAtmList.iloc[i,0],self.filterAtmList.iloc[i,1],self.filterAtmList.iloc[i,2],
                                     self.filterAtmList.iloc[i,3],self.filterAtmList.iloc[i,4],self.filterAtmList.iloc[i,5],
                                     self.filterAtmList.iloc[i,6],self.filterAtmList.iloc[i,7],self.filterAtmList.iloc[i,8],
                                     self.filterAtmList.iloc[i,9],self.filterAtmList.iloc[i,10],
                                     self.filterAtmList.iloc[i,11],self.filterAtmList.iloc[i,12]],
                             tags=self.filterAtmList.index[i]
                            )  
            
        # display to TkinterMapView 
        self.markerNow.delete()
        self.markerNow = self.resultTkinterMapView.set_position(self.latitude, self.longitude, text_color = 'darkRed', marker=True)
        self.markerNow.set_text(self.addressSelectValue)
        self.tree.bind('<<TreeviewSelect>>',self.treeSelected) 

    def treeSelected(self,event):       
        selectedTree = event.widget  

        # get Longitude & Latitude of selected address
        itemTage = selectedTree.selection()[0]            #selectedTree.selection()=('I005',)
        itemDic = selectedTree.item(itemTage)             #{'text': '', 'image': '', 'values': [812, '台新東高雄', ...], 'open': 0, 'tags': [5831]}
        indexIndicater = itemDic['tags'][0]
        selectedData = self.filterAtmList.loc[indexIndicater]
        selectedPlaceLongitude = selectedData[13]
        selectedPlaceLatitude = selectedData[14]     

        # 於地圖上標記地址----------------------------------
        self.markerATM = self.resultTkinterMapView.set_position(selectedPlaceLatitude, selectedPlaceLongitude, text_color = 'darkBlue', marker=True)   
        self.markerATM.set_text(selectedData[7])
  





        

def main(): 
    
    # get atmData from internet--------------------   
    dataSource.DownLoadAtmData()    
    
    # build window()-------------------------------
    atmData = pd.read_csv('atmData.csv')

    window = Window(atmData)
    window.title("ATM裝設地點-個人/企業版: ATM地點查詢")    
    window.geometry("1270x680")
    window.mainloop()   
    

if __name__=="__main__":
    main()