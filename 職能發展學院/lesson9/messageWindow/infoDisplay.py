from tkinter.simpledialog import Dialog

class InfoDisplay(Dialog):

    def __init__(self,parent,title=None,info=None): #自訂的初始化
        print(title)
        if info is not None:
            self.info = info
        super().__init__(parent,title)

    def body(self,master):
        print("master:",master)
        print("傳過來的資料:",self.info)


    #def buttonbox(self):
    #    pass

