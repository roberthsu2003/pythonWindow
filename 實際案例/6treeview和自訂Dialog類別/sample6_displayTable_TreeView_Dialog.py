import tkinter as tk
from tkinter import ttk
import csv
from tkinter.simpledialog import Dialog
from PIL import ImageTk,Image
import os

class Window(tk.Tk):
    def __init__(self):
        super().__init__();
        self.title("讀取pchone24.csv")
        self.style = ttk.Style(self)
        self.datas = read_csv("pchone24.csv")
        self.treeView = ttk.Treeview(self, columns=('#1','#2','#3', '#4', '#5', '#6', '#7'),show='headings')
        self.treeView.heading('#1',text='產品類型')
        self.treeView.heading('#2', text='產品名稱')
        self.treeView.heading('#3', text='產品網址')
        self.treeView.heading('#4', text='圖片網址')
        self.treeView.heading('#5', text='圖片名稱')
        self.treeView.heading('#6', text='產品資訊')
        self.treeView.heading('#7', text='產品價格')
        self.treeView.grid(row=0, column=0, sticky='nsew')
        self.treeView.bind("<<TreeviewSelect>>",self.item_selected)

        for _ in range(10):
            for data in self.datas[1:]:
                self.treeView.insert('',tk.END,values=data)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeView.yview)
        self.treeView.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0,column=1,sticky='ns')


    def item_selected(self,event):
        #selection()取出的為一個元素的tuple
        #item(rowID)
        #取出的item為Dictionary)
        item = self.treeView.item(self.treeView.selection()[0])
        record = item['values']
        #showinfo(title='選取資訊',message=','.join(record))
        message = ShowInfo(self,info = record)

class ShowInfo(Dialog):
    def __init__(self, parent, title=None, info=None):
        self.info = info #必需要寫在前面
        super().__init__(parent,title)


    def body(self, master):
        print(self.info)
        self.title(self.info[1])

        tk.Label(master, text='產品類型:').grid(row=0, sticky=tk.W)
        tk.Label(master, text='產品名稱:').grid(row=1, sticky=tk.W)
        tk.Label(master, text='產品網址:').grid(row=2, sticky=tk.W)
        tk.Label(master, text='圖片網址').grid(row=3, sticky=tk.W)
        tk.Label(master, text='圖片名稱').grid(row=4, sticky=tk.W)
        tk.Label(master, text='產品資訊').grid(row=5, sticky=tk.W)
        tk.Label(master, text='產品價格').grid(row=6, sticky=tk.W)

        for index,infoText in enumerate(self.info):
            tk.Label(master,text=infoText).grid(row=index,column=1,sticky=tk.W)

        print(os.path.abspath("photos/"+self.info[4]))
        imagePath = os.path.abspath("photos/"+self.info[4])
        img = ImageTk.PhotoImage(Image.open(imagePath))
        picLabel = tk.Label(master,image=img)
        #要加下面這行才會顯示
        picLabel.image = img
        picLabel.grid(row=7,column=1, sticky=tk.W)

        return None

    def buttonbox(self):
        '''add standard button box.
        override if you do not want the standard buttons
        '''

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)


        self.bind("<Return>", self.ok)
        box.pack()

    def apply(self):
        print('apply')



def read_csv(fileName):
    try:
        fileObject = open(fileName,'r',encoding='utf8')
    except Exception as e:
        print("讀取錯誤")
        fileObject.close()
        return None

    csvReaderObject = csv.reader(fileObject)
    return list(csvReaderObject)



if __name__ == "__main__":
    window = Window()
    window.mainloop()