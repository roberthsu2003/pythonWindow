from tkinter.simpledialog import Dialog
from tkinter import ttk
from tkinter import Misc
import tkinter as tk

class CustomMessagebox(Dialog):    
    def __init__(self, parent:Misc, title:str,name:str,bmi:float,status:str,advice:str,status_color:str):        
        self.parent = parent
        self.name = name
        self.bmi = bmi
        self.status = status
        self.advice = advice
        style = ttk.Style()
        style.configure('status.TLabel',foreground=status_color)
        super().__init__(parent=parent, title=title)

    def body(self, master):
        # 創建對話框主體。返回應具有初始焦點的控件。
        contain_frame = ttk.Frame(master,style='Input.TFrame')
        # 姓名
        label_name = ttk.Label(contain_frame, text="姓名:")
        label_name.grid(row=0, column=0, padx=5, pady=5,sticky=tk.E)

        self.value_name = ttk.Label(contain_frame,text=self.name)
        self.value_name.grid(row=0, column=1, padx=5, pady=5)

        # bmi
        label_bmi = ttk.Label(contain_frame, text="BMI值:")
        label_bmi.grid(row=1, column=0, padx=5, pady=5,sticky=tk.E)

        self.value_height = ttk.Label(contain_frame,text=f'{self.bmi:.2f}')
        self.value_height.grid(row=1, column=1, padx=5, pady=5)

        # status
        label_status = ttk.Label(contain_frame, text="狀態:")
        label_status.grid(row=2, column=0, padx=5, pady=5,sticky=tk.E)

        self.value_status = ttk.Label(contain_frame,text=self.status,style='status.TLabel')
        self.value_status.grid(row=2, column=1, padx=5, pady=5)

        #advice
        label_advice = ttk.Label(contain_frame, text="建議:")
        label_advice.grid(row=3, column=0, padx=5, pady=5,sticky=tk.E)

        self.value_advice = ttk.Label(contain_frame,text=self.advice)
        self.value_advice.grid(row=3, column=1, padx=5, pady=5)   

        contain_frame.pack(pady=10,padx=30)

    def apply(self):
        # 當用戶按下確定時處理數據
        self.parent.name_value.set('')
        self.parent.hight_value.set('')
        self.parent.weight_value.set('')

    def buttonbox(self):
        # Add custom buttons (overriding the default buttonbox)
        box = ttk.Frame(self)
        self.ok_button = tk.Button(box, text="確定", width=10, command=self.ok, default=tk.ACTIVE)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()

    def ok(self):
        # Override the ok method
        print("OK button was clicked!")
        super().ok()


    