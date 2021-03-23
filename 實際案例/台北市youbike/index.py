import dataSource
import tkinter as tk
import tkinter.ttk as ttk
import threading


class YoubikeWindow(tk.Tk):
    defaultArea = '文山區'
    def __init__(self):
        super().__init__()
        self.title("台北市youbike及時資訊")
        mediumFont = {'font':('Arial', 20)}
        s = ttk.Style()
        s.configure('Red.TLabelframe.Label', font=('Arial', 20))


        #display interface
        #leftSide
        leftFrame = ttk.LabelFrame(self,text='台北市行政區',style='Red.TLabelframe')
        areaList = tk.Listbox(leftFrame,height=12,selectbackground='#888888',**mediumFont)
        areaList.bind('<<ListboxSelect>>',self.userSelected)
        for name in dataSource.areas:
            areaList.insert(tk.END,name)
        areaList.pack(padx=10,pady=10)
        leftFrame.pack(side=tk.LEFT,padx=30,pady=30)

        #rightSide
        rightFrame= tk.Frame(self)
        infoCanvas = dataSource.getInfoCanvas(rightFrame)
        infoCanvas.pack(anchor=tk.NE)
        self.infoFrame = ttk.LabelFrame(rightFrame,text='文山區',style='Red.TLabelframe')
        self.infoFrame.pack(padx=20,pady=20)
        rightFrame.pack(side=tk.RIGHT,fill=tk.Y)

        #進入時,右邊顯示的區域

        #simpleInfo = dataSource.getAreaSimpleInfo('文山區')
        #self.changeDisplayOfRightSide(simpleInfo,'文山區')
        self.updateDownloadData()

    def userSelected(self,event):
        listbox = event.widget
        areaName = listbox.get(listbox.curselection())
        YoubikeWindow.defaultArea = areaName
        #得到選取區域的簡單資料
        #simpleInfo內容是list,裏面有tuple(站名,顏色)
        simpleInfo = dataSource.getAreaSimpleInfo(areaName)

        #改變右邊的區域內容,呼叫method,並傳送資料
        self.changeDisplayOfRightSide(simpleInfo, areaName)


    def changeDisplayOfRightSide(self,info,lableName):
        # info內容是list,裏面有tuple(站名,顏色)
        #先清除self.infoFrame內的內容

        self.infoFrame.configure(text=lableName)
        for widget in self.infoFrame.winfo_children():
            widget.destroy()


        for index,siteInfo in enumerate(info):
            #一個row,5個cell
            if index % 5 == 0:
                #每5個cell,要有一個parentFrame
                parentFrame = tk.Frame(self.infoFrame)
                parentFrame.pack(anchor=tk.W,padx=20)

            #建立一個frame,內有canvas的圓點和button
            cellFrame = tk.Frame(parentFrame, bg='#cccccc', width=150, height=40, borderwidth=1, relief=tk.GROOVE)
            #建立圓點
            #siteInfo是tuple
            dataSource.getColorCircle(cellFrame,siteInfo[1]).pack()
            nameButton = tk.Button(cellFrame,text=siteInfo[0],width=20,font=(13,))
            nameButton.bind('<Button-1>',self.buttonAction)
            nameButton.pack()

            cellFrame.pack(side=tk.LEFT)

    def buttonAction(self,event=None):
        #使用cget('text'),取出button的text
        siteName = event.widget.cget('text')

        #取出單一站點detail資料
        #print(dataSource.getDetailInfoOfSite(siteName))
        info = dataSource.getDetailInfoOfSite(siteName)
        singleSiteInfo = dataSource.SingleSiteInfo(self,title="站場資訊",info=info)

    def updateRightSideContent(self):
        simpleInfo = dataSource.getAreaSimpleInfo(YoubikeWindow.defaultArea)
        self.changeDisplayOfRightSide(simpleInfo, YoubikeWindow.defaultArea)

    def updateDownloadData(self):
        #重新下載
        print('重新下載')
        dataSource.loadDataFromYouBikeTP()
        #更新右邊畫面
        self.updateRightSideContent()
        self.t = threading.Timer(1*60,self.updateDownloadData)
        self.t.start()



def closeWindow():
    window.destroy()
    window.t.cancel()



if __name__ == "__main__":
    window = YoubikeWindow()
    window.protocol("WM_DELETE_WINDOW",closeWindow)
    window.mainloop()
