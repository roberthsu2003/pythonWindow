#!usr/bin/python3.8
"""
這是我的python_window範例
"""
import tkinter as tk

def createdWindow():
    window = tk.Tk()
    window.title("我的第一個視窗")
    window.geometry('600x300+200+200')
    window.resizable(False,False)
    window.mainloop()

if __name__ == "__main__":
    createdWindow()



