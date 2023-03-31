# Draw Captain America's shield (畫美國隊長盾牌)
import tkinter
import math
root = tkinter.Tk()
root.geometry("1280x960")
canv = tkinter.Canvas(root, width=1280, height=960)
canv.pack()
x_center, y_center, r = 640, 480, 180
canv.create_oval(x_center+5*90, y_center+5*90, x_center-5*90, y_center-5*90, fill='red', outline='red', width=0)
canv.create_oval(x_center+4*90, y_center+4*90, x_center-4*90, y_center-4*90, fill='silver', outline='silver', width=0)
canv.create_oval(x_center+3*90, y_center+3*90, x_center-3*90, y_center-3*90, fill='red', outline='red', width=0)
canv.create_oval(x_center+2*90, y_center+2*90, x_center-2*90, y_center-2*90, fill='blue', outline='blue', width=0)
x_star, y_star = [], []
for i in range(5):
    x_star.append(x_center+r*math.cos((18+i*72)*math.pi/180))
    y_star.append(y_center+r*math.sin((18+i*72)*math.pi/180))
canv.create_polygon(x_star[0], y_star[0], x_star[2], y_star[2], x_star[4], y_star[4], x_star[1], y_star[1], x_star[3], y_star[3], fill="white", outline="white", width=0)
root.mainloop()
