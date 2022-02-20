#!usr/bin/python3.8
"""
這是我的python_window範例
"""
import tkinter as tk
from tkinter import ttk

def createdWindow():
    window = tk.Tk()
    window.configure(bg='white')
    window.title("我的第一個視窗")
    #window.geometry('600x300+200+200')
    window.resizable(False,False)
    mainFrame = tk.Frame(window)
    label = tk.Label(window, text="Hello World")
    label.pack(fill=tk.BOTH, expand=1, padx=100, pady=100)
    mainFrame.pack()

    window.mainloop()

if __name__ == "__main__":
    createdWindow()



