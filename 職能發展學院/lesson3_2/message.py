from tkinter.simpledialog import Dialog

class MapDialog(Dialog):
    def __init__(self, parent, title = None,info=None):
        self.info = info
        super().__init__(parent,title=title)


    def body(self, master):
        print("body")
        print(self.info)

    def buttonbox(self):
        super().buttonbox()
        print("自訂按鈕區")


