import tkinter
from tkinter import *

reset = True

#主計算程式
def Calculate(event):
  global label
  global reset

  try:
    num = event.widget['text']
    if num == 'C':
      label['text'] = "0"
      return
    if num == "=":
      label['text'] = str(eval(label['text']))
      reset = True
      return
    s = label['text']
    if s == '0' or reset == True:
      s = ""
      reset = False
    label['text'] = s + num
  except:
    label['text'] = '輸入錯誤'

#主視窗
window = Tk()
window.title('計算機')

#顯示屏

mainframe = tkinter.Frame(window, bg='pink')

label = Label(mainframe, text="0", font=('arial', 12), background="lightblue", anchor=E)
label['width'] = 37
label['height'] = 1
label.grid(row=0, columnspan=4, padx=2, pady=2, sticky=W)

#按鍵
showText1 = "789/456*123-0.C+"
for i in range(4):
  for j in range(4):
    b=Button(mainframe, text=showText1[i*4+j], width=10)
    b.grid(row=i+2, column=j, padx=2, pady=2)
    b.bind("<Button-1>", Calculate)

showText2 = "()"
for i in range(2):
  b=Button(mainframe, text=showText2[i], width=10)
  b.grid(row=6, column=2+i, padx=2, pady=2)
  b.bind("<Button-1>", Calculate)

b = Button(mainframe, text="=")
b.grid(row=6, columnspan=2, sticky="we")
b.bind("<Button-1>", Calculate)

mainframe.pack(padx=5, pady=5)

if __name__ == '__main__':
    window.mainloop()