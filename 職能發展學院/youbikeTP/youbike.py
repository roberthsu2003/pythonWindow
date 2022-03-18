import dataSource
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        #上方的Frame=========start
        topFrame = tk.Frame(self,background='red')
        tk.Label(topFrame,text="台北市youbike即時監測系統",font=("arial",20)).pack()
        topFrame.grid(column=0,row=0,columnspan=3,padx=20,pady=20)
        #上方的Frame=========end
        self.leftLabelFrame = LeftLabelFrame(self,text="左邊的")
        self.leftLabelFrame.grid(column=0,row=1,padx=20,pady=20)

        self.centerLabelFrame = CenterLabelFrame(self,text="中間的")
        self.centerLabelFrame.grid(column=1,row=1,padx=20,pady=20)

        self.rightLabelFrame = RightLabelFrame(self,text="右邊的")
        self.rightLabelFrame.grid(column=2, row=1, padx=20, pady=20)
        self.update_data()


    def update_data(self):
        dataSource.update_youbike_data()
        self.leftLabelFrame.update_screen()
        self.rightLabelFrame.update_screen()
        self.centerLabelFrame.update_screen()
        self.after(60*1000,self.update_data)

class LeftLabelFrame(tk.LabelFrame):
    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        topFrame = tk.Frame(self,background='gray')
        tk.Label(topFrame, text="正常租借站點", font=("arial", 20),background='gray',fg="white").pack(padx=10,pady=10)
        normal_count = dataSource.get_count_of_normal()
        tk.Label(topFrame, text=f"數量:{normal_count}",background='gray',fg='#ffffff', font=("arial",20)).pack(padx=10,pady=10)
        topFrame.pack(pady=20)
        treeView = ttk.Treeview(self,columns=('sna','tot','sbi','bemp'),show="headings")
        treeView.heading('sna',text='名稱')
        treeView.heading('tot', text='總數')
        treeView.heading('sbi', text='可借')
        treeView.heading('bemp', text='可還')

        treeView.column('sna',width=200)
        treeView.column('tot',width=50)
        treeView.column('sbi',width=50)
        treeView.column('bemp',width=50)
        treeView.pack()

        normal_list = dataSource.get_list_of_normal()
        for item in normal_list:
            treeView.insert('', 'end', values=item)

    def update_screen(self):
        print("L update")



class CenterLabelFrame(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        topFrame = tk.Frame(self, background='gray')
        tk.Label(topFrame, text="可借車量小於4台站點", font=("arial", 20), background='gray', fg="white").pack(padx=10, pady=10)
        lessbike_count = dataSource.get_count_of_less_bike()
        tk.Label(topFrame, text=f"數量:{lessbike_count}", background='gray', fg='#ffffff', font=("arial", 20)).pack(padx=10,
                                                                                                                pady=10)
        topFrame.pack(pady=20)
        treeView = ttk.Treeview(self, columns=('sna', 'tot', 'sbi', 'bemp'), show="headings")
        treeView.heading('sna', text='名稱')
        treeView.heading('tot', text='總數')
        treeView.heading('sbi', text='可借')
        treeView.heading('bemp', text='可還')

        treeView.column('sna', width=200)
        treeView.column('tot', width=50)
        treeView.column('sbi', width=50)
        treeView.column('bemp', width=50)
        treeView.pack()

        lessbike_list = dataSource.get_list_of_less_bike()
        for item in lessbike_list:
            treeView.insert('', 'end', values=item)

    def update_screen(self):
        print("C update")

class RightLabelFrame(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        topFrame = tk.Frame(self, background='gray')
        tk.Label(topFrame, text="還車數量少於4台站點", font=("arial", 20), background='gray', fg="white").pack(padx=10, pady=10)
        backspace_count = dataSource.get_count_of_less_back_space()
        tk.Label(topFrame, text=f"數量:{backspace_count}", background='gray', fg='#ffffff', font=("arial", 20)).pack(padx=10,
                                                                                                                pady=10)
        topFrame.pack(pady=20)
        treeView = ttk.Treeview(self, columns=('sna', 'tot', 'sbi', 'bemp'), show="headings")
        treeView.heading('sna', text='名稱')
        treeView.heading('tot', text='總數')
        treeView.heading('sbi', text='可借')
        treeView.heading('bemp', text='可還')

        treeView.column('sna', width=200)
        treeView.column('tot', width=50)
        treeView.column('sbi', width=50)
        treeView.column('bemp', width=50)
        treeView.pack()

        less_back_space_list = dataSource.get_list_of_less_back_space()
        for item in less_back_space_list:
            treeView.insert('', 'end', values=item)

    def update_screen(self):
        print("R update")

if __name__=="__main__":
    dataSource.update_youbike_data()
    window = Window()
    window.title("台北市youbike及時監測資料")
    window.mainloop()
