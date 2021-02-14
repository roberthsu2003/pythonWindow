import tkinter
from tkinter import ttk

win = tkinter.Tk()
win.title("Combobox下拉框")
win.geometry("800x600+600+100")

cv= tkinter.StringVar()
com=ttk.Combobox(win,textvariable=cv)
com.pack()
#設置下拉數據
com["value"]=("福建","江西","浙江")

#設置默認值
com.current(0)

#綁定事件
def func(event):
    print(com.get())
    print(cv.get())
    print("tom is a boy")
com.bind("<<ComboboxSelected>>",func) #等同於textvariable=cv這個變量

win.mainloop()