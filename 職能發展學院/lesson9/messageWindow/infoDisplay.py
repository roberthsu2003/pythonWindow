import tkinter as tk
from tkinter.simpledialog import Dialog

class InfoDisplay(Dialog):

    def __init__(self,parent,title=None,info=None): #自訂的初始化
        print(title)
        if info is not None:
            self.info = info
        super().__init__(parent,title)

    def body(self,master):
        topFrame=tk.Frame(master,bg='#999999')
        leftFrame = tk.Frame(topFrame,width=100,height=200,bg='#aaaaaa')
        listbox = tk.Listbox(leftFrame)
        for item in self.info:
            listbox.insert(tk.END, item[0])


        listbox.pack(side=tk.LEFT)
        leftFrame.pack_propagate(0)
        leftFrame.pack(side=tk.LEFT)
        #topFrame.pack_propagate(0)
        topFrame.pack()

        print("master:",master)
        print("傳過來的資料:",self.info)


    #def buttonbox(self):
    #    pass

