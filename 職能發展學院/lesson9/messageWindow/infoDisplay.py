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
        leftFrame = tk.Frame(topFrame,bg='#aaaaaa')
        scrollBar = tk.Scrollbar(leftFrame, orient=tk.VERTICAL)
        scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        listbox = tk.Listbox(leftFrame,yscrollcommand=scrollBar.set)
        scrollBar.config(command=listbox.yview)
        for item in self.info:
            listbox.insert(tk.END, item[0])
        listbox.bind("<<ListboxSelect>>",self.onSelect)
        listbox.pack(side=tk.LEFT,fill=tk.Y)

        #leftFrame.pack_propagate(0)
        leftFrame.pack(side=tk.LEFT,fill=tk.Y)
        #topFrame.pack_propagate(0)

        rightFrame = tk.Frame(topFrame, bg='#555555',width=700,height=200)
        rightFrame.pack(side=tk.RIGHT)
        rightFrame.pack_propagate(0)
        topFrame.pack()

        print("master:",master)
        print("傳過來的資料:",self.info)

    def onSelect(self,event):
        widget = event.widget
        index = widget.curselection()[0]
        year = widget.get(index)
        print(year)



    #def buttonbox(self):
    #    pass

