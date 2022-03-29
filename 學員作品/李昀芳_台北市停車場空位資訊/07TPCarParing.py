import requests
import tkinter as tk
from tkinter.font import Font


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #取得網路上的資料
        res = requests.get('https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_alldesc.json')
        jsonObj1 = res.json()
        parking_data = jsonObj1['data']['park']

        res = requests.get('https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json')
        jsonObj2 = res.json()
        self.updated_time = jsonObj2['data']["UPDATETIME"]
        self.available_data = jsonObj2['data']['park']
        self.selected_ids = [ad['id'] for ad in self.available_data]
        self.selected_parking_data = [p for p in parking_data if p['id'] in self.selected_ids]

        self.district_id_name = {}
        for pd in self.selected_parking_data:
            if (pd['id'] in self.selected_ids):
                if pd['area'] in self.district_id_name:
                    self.district_id_name[pd['area']].append((pd['id'], pd['name']))
                else:
                    self.district_id_name[pd['area']] = [(pd['id'], pd['name'])]
        
        
        areas = ['中正區', '大同區', '中山區', '萬華區', 
        '信義區', '松山區', '大安區', '南港區', 
        '北投區', '內湖區', '士林區', '文山區']

        #介面
        self.title("台北市行政區")
        leftFrame = tk.Frame(self, bd=2, relief=tk.GROOVE, padx=10, pady=7)
        buttonFont = Font(family='標楷體', size=16)

        for index, area in enumerate(areas):
            if index % 1 == 0:
                parentframe = tk.Frame(leftFrame)
                parentframe.pack(pady=(0,3))
            btn = tk.Button(parentframe, text=area, font=buttonFont, bg="gray9",fg="white",padx=5, pady=8)
            btn.bind('<Button-1>', self.userClick)
            btn.pack(side=tk.LEFT, padx=5)
        leftFrame.pack(side=tk.LEFT,padx=10, pady=(0,10))




        #建立下方radioButton的介面
        self.fixedWidthFrame = tk.Frame(self,height=600)
        self.createdRadioButtonFrame()
        self.fixedWidthFrame.pack(padx=20)

        #建立message介面
        messageDisplayFrame = tk.Frame(self,bd=2,relief=tk.GROOVE,padx=20,pady=10)
        self.mdayLabel = tk.Label(messageDisplayFrame, text="記錄時間:")
        self.mdayLabel.pack(anchor=tk.W)
        self.nameLabel = tk.Label(messageDisplayFrame,text="站名:")
        self.nameLabel.pack(anchor=tk.W)
        self.arLabel = tk.Label(messageDisplayFrame,text="地址:")
        self.arLabel.pack(anchor=tk.W)
        self.totcarLabel = tk.Label(messageDisplayFrame, text="總汽車空位數:")
        self.totcarLabel.pack(anchor=tk.W)
        self.carempLabel = tk.Label(messageDisplayFrame, text="汽車剩餘空位數量:")
        self.carempLabel.pack(anchor=tk.W)
        self.totmotorLabel = tk.Label(messageDisplayFrame, text="總機車空位數:")
        self.totmotorLabel.pack(anchor=tk.W)
        self.motorempLabel = tk.Label(messageDisplayFrame, text="機車剩餘空位數量:")
        self.motorempLabel.pack(anchor=tk.W)
        messageDisplayFrame.pack(expand=True,fill=tk.BOTH,padx=20,pady=20)




    def userClick(self,event):
        self.bottomFrame.destroy()
        self.selectedArea = event.widget['text']

        park_name_lst = [p[1] for p in self.district_id_name[self.selectedArea]]
        self.createdRadioButtonFrame(data=park_name_lst)

    def createdRadioButtonFrame(self,data=None):
        self.bottomFrame = tk.Frame(self.fixedWidthFrame, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        if data == None:
            self.radioButtonData = []
        else:
            self.radioButtonData = data
        self.stringVar = tk.StringVar()

        for index, data in enumerate(self.radioButtonData):
            if index % 18== 0:
                parentframe = tk.Frame(self.bottomFrame)
                parentframe.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
            radioButton = tk.Radiobutton(parentframe, text=data, value=data, variable=self.stringVar,command=self.userChoicedRadioButton).pack(anchor=tk.W)
        self.bottomFrame.pack(pady=(0,10))
        self.stringVar.set(0)

    def userChoicedRadioButton(self):

        park_lot_name = self.stringVar.get()
        park_lot_id = 0

        for p in self.district_id_name[self.selectedArea]:
            if p[1] == park_lot_name:
                park_lot_id = p[0]

        data = [p for p in self.selected_parking_data if p['id'] == park_lot_id][0]
        avail_data = [p for p in self.available_data if p['id'] == park_lot_id][0]
        print(data)
        print(avail_data)

        
        self.mdayLabel["text"] = "記錄時間: {}".format(self.updated_time)
        self.nameLabel["text"] = "站名: {}".format(park_lot_name)
        self.arLabel["text"] = "地址: {}".format(data['address'])

        availablecar = avail_data['availablecar']
        if availablecar == -9:
            availablecar = "目前無法取得即時資訊"
        self.carempLabel["text"] = "汽車剩餘空位數量: {}".format(availablecar)

        availablemotor = avail_data['availablemotor']
        if availablemotor == -9:
            availablemotor = "目前無法取得即時資訊"
        self.motorempLabel["text"] = "機車剩餘空位數量: {}".format(availablemotor)

        self.totcarLabel["text"] = "總汽車空位數: {}".format(data['totalcar'])
        self.totmotorLabel["text"] = "總機車空位數: {}".format(data['totalmotor'])

        

if __name__ == "__main__":
    window = Window()
    window.geometry("+50+0")
    window.mainloop()