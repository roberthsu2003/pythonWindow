import tkinter as tk
from PIL import Image,ImageTk

root = tk.Tk()
root.title('均價線圖')
root.geometry('640x480')
#-----打開圖檔並且重新設定圖片大小
mov_img=Image.open('mov.jpeg')
#mov_img=mov_img.resize((500,250))

#-----把圖片轉換為tkinter可辨識
tk_img=ImageTk.PhotoImage(mov_img)

#----設定canvas畫布大小及圖片放置位子
canvas = tk.Canvas(root, width=640, height=480)  # 加入 Canvas 畫布，並設定畫布大小
canvas.create_image(0,0,anchor='nw',image=tk_img) #設定以“n(上)w(左)”為畫布起始點
canvas.pack()

root.mainloop()