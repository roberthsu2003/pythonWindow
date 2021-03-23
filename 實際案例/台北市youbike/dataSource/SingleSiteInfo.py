from tkinter.simpledialog import Dialog
import tkinter as tk

class SingleSiteInfo(Dialog):
    def __init__(self, parent, title=None, info=None):
        self.info = info #必需要寫在前面
        super().__init__(parent,title)

    def body(self, master):
        '''
        create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        print(self.info)
        fontStyle = {'font':('arial',13)}
        tk.Label(master, text=f'站場編號:{self.info["sno"]}', **fontStyle).grid(row=0, sticky=tk.W)
        tk.Label(master, text=f'站場名稱:{self.info["sna"]}', **fontStyle).grid(row=1, sticky=tk.W)
        tk.Label(master, text=f'車輛總數:{self.info["tot"]}', **fontStyle).grid(row=2, sticky=tk.W)
        tk.Label(master, text=f'可借車數:{self.info["sbi"]}', **fontStyle).grid(row=3, sticky=tk.W)
        tk.Label(master, text=f'站場地址:{self.info["ar"]}', **fontStyle).grid(row=4, sticky=tk.W)
        tk.Label(master, text=f'可還車位:{self.info["bemp"]}', **fontStyle).grid(row=5, sticky=tk.W)
        if self.info['act'] == '1':
            state = '營運中'
        else:
            state = '維修中'
        tk.Label(master, text=state,**fontStyle).grid(row=6, sticky=tk.W)

    def buttonbox(self):
        '''
        add standard button box.
        如果不要使用正常的按鈕,必需覆寫這個method
         '''
        box = tk.Frame(self)
        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        box.pack()