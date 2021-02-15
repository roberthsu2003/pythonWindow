import tkinter as tk
from tkinter import  ttk
import csv
from tkinter.messagebox import showinfo

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
        dialog = ShowDialog(self,'測試',['one','two'])


class ShowDialog:
    def closeWindow(self):

        self.subWindow.destroy()


    def __init__(self,root,message, options):
        self.subWindow = tk.Toplevel(root)
        self.subWindow.geometry('300x300')
        self.subWindow.transient()
        tk.Label(self.subWindow, text=message).pack()
        for item in options:
            ttk.Button(self.subWindow, text=item, command=self.closeWindow).pack()
        #self.subWindow.mainloop()


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