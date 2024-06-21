import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from tools import CustomMessagebox

class Window(ThemedTk):
    def __init__(self,theme:str|None,**kwargs):
        super().__init__(**kwargs)
        self.title("BMI計算器")
        #self.configure(bg="#D3D3D3")
        #self.geometry("350x350+100+50")
        self.resizable(False,False)
        style = ttk.Style()
        style.configure('input.TFrame',background='#ffffff')
        style.configure('press.TButton',font=('arial',16))
        #========================
        titleFrame = ttk.Frame(self)
        title_label = ttk.Label(self, text="BMI計算器", font=("Arial", 20))
        title_label.pack(pady=10)
        titleFrame.pack(padx=100,pady=(0,20))
        #========================
        input_frame = ttk.Frame(self,style='Input.TFrame')
        # 姓名
        label_name = ttk.Label(input_frame, text="姓名:")
        label_name.grid(row=0, column=0, padx=5, pady=5,sticky=tk.E)

        self.name_value = tk.StringVar()
        self.name_value.set('')
        entry_name = ttk.Entry(input_frame,textvariable=self.name_value)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        # 身高體重
        label_height = ttk.Label(input_frame, text="身高 (cm):")
        label_height.grid(row=1, column=0, padx=5, pady=5,sticky=tk.E)

        self.hight_value = tk.StringVar()
        self.hight_value.set('')
        entry_height = ttk.Entry(input_frame,textvariable=self.hight_value)
        entry_height.grid(row=1, column=1, padx=5, pady=5)

        label_weight = ttk.Label(input_frame, text="體重 (kg):")
        label_weight.grid(row=2, column=0, padx=5, pady=5,sticky=tk.E)

        self.weight_value = tk.StringVar()
        self.weight_value.set('')
        entry_weight = ttk.Entry(input_frame,textvariable=self.weight_value)
        entry_weight.grid(row=2, column=1, padx=5, pady=5)    

        input_frame.pack(pady=10,padx=30)
        #===================================
        button_frame = ttk.Frame(self)
        button_calculate = ttk.Button(button_frame, text="計算", command=self.show_bmi_result,style='press.TButton')
        button_calculate.pack(side=tk.RIGHT,expand=True,fill=tk.X)

        button_close = ttk.Button(button_frame, text="關閉",command=self.destroy,style='press.TButton')
        button_close.pack(side=tk.LEFT,expand=True,fill=tk.X)
        button_frame.pack(padx=20,fill=tk.X,pady=(0,15))

    
    
    def show_bmi_result(self):
        try:
            name:str = self.name_value.get()
            height:int = int(self.hight_value.get())
            weight:int = int(self.weight_value.get())
        
        #except UnboundLocalError:
            #messagebox.showwarning("Warning","欄位沒有填寫")
        except ValueError:
            messagebox.showwarning("Warning","格式錯誤,欄位沒有填寫")
        except Exception:
            messagebox.showwarning("Warning","不知明的錯誤")
        else:
            self.show_result(name=name,height=height,weight=weight)


    def show_result(self,name:str,height:int,weight:int):
            bmi = weight / (height / 100) ** 2
            if bmi < 18.5:
                status = "體重過輕"
                ideal_weight = 18.5 * (height / 100) ** 2
                weight_change = ideal_weight - weight
                status_color = "red"
                advice = f"您需要至少增加 {abs(weight_change):.2f} 公斤才能達到正常體重。"
            elif 18.5 <= bmi <= 24.9:
                status = "正常"
                status_color = "blue"
                advice = "您的體重正常，請保持！"
            else:
                status = "體重過重"
                ideal_weight = 24.9 * (height / 100) ** 2
                weight_change = weight - ideal_weight
                status_color = "red"
                advice = f"您需要至少減少 {abs(weight_change):.2f} 公斤才能達到正常體重。"

            CustomMessagebox(self,title="BMI",name=name,bmi=bmi,status=status,advice=advice,status_color=status_color)
            
            
            

def main():
    window = Window(theme='arc')
    window.mainloop()

if __name__ == '__main__':
    main()