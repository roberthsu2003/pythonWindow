'''
專案在學習grid的編排
'''

import tkinter as tk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


def main():
    '''
    這是程式的執行點
    '''
    window = Window()
    window.title("BMI計算")
    window.geometry("400x500")
    window.mainloop()

if __name__ == "__main__":
    main()