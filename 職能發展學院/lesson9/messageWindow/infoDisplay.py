from tkinter.simpledialog import Dialog

class InfoDisplay(Dialog):

    def __init__(self,parent,title=None): #自訂的初始化
        print(title)
        super().__init__(parent,title)

