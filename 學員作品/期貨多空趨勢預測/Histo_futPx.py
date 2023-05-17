import tkinter as tk
from tkinter import ttk
import Histo_stocksPx


start_date = Histo_stocksPx.start_date

class ComboFrame(ttk.Frame):
    def __init__(self, master,**kwargs): 
        super().__init__(master, **kwargs)
        global start_date
# create custom style object
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('default')

#建一個combobox----------------------------------------------
        comboBoxFrame = ttk.Frame(self,style='back.TFrame')
        comboBoxFrame.pack(side='left',expand=True,fill=tk.BOTH) 

        self.comboBoxValues = ['請選擇期貨交易商品 :',
                                '台指期近月',
				'電子期近月',
                                '金融期近月'] 
# create combobox with custom style
        self.comboBox = ttk.Combobox(comboBoxFrame,values=self.comboBoxValues,state='readonly')
        self.comboBox['style'] = 'Custom.TCombobox'
        ttkStyle.map('Custom.TCombobox', fieldbackground=[('readonly', '#B0CFDE')], foreground=[('readonly', '#52595D')])
        
        # Set the font of the dropdown list to Arial 12
        #self.comboBox.option_add('*TCombobox*Listbox*Font',('Helvetica', 10,'bold'))

        self.comboBox.current(0) #將顯示設為第一個"請選擇期貨交易商品"
        self.comboBox.pack(side='left')
        #self.comboBox.bind('<<ComboboxSelected>>', self.futures_changed)




