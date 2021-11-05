import tkinter as tk

class Dialog(tk.Toplevel):
    def __init__(self,root,title,total):
        super().__init__(root)
        self.transient(root)
        #self.geometry('200x200')
        tk.Label(self,text=title).pack(pady=20,padx=50)
        print(total)
        tk.Label(self,text=f'{title}:{total}').pack(pady=20,padx=50)
        tk.Button(self,text="關閉",command=self.closeWindow).pack(pady=20)

    def closeWindow(self):
        self.destroy()