from tkinter.simpledialog import Dialog
import tkintermapview as tkmap
import tkinter as tk

class MapDialog(Dialog):
    def __init__(self, parent, title = None,info=None):
        self.info = info
        super().__init__(parent,title=title)


    def body(self, master):
        map_widget = tkmap.TkinterMapView(master,
                                          width=800,
                                          height=600,
                                          corner_radius=0
                                          )
        map_widget.pack()

    def buttonbox(self):
        #super().buttonbox()
        #自訂按鈕區
        bottomFrame = tk.Frame(self)
        closeButton = tk.Button(bottomFrame,text="關閉"+self.title()+"地圖",command=self.ok)
        closeButton.pack()
        bottomFrame.pack()


    def ok(self, event=None):
        super().ok()


