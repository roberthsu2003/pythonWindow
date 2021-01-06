from tkinter import *
from PIL import Image, ImageTk
import os


class Scrapbook:
    def __init__(self, master=None):
        self.master = master
        self.frame = Frame(master, width=400, height=420, bg='gray50',
                           relief=RAISED, bd=4)

        self.lbl = Label(self.frame)
        self.lbl.place(relx=0.5, rely=0.48, anchor=CENTER)

        self.images = []
        images = os.listdir("./images")

        xpos = 0.05
        for i in range(10):
            Button(self.frame, text='%d' % (i + 1), bg='gray10',
                   fg='white', command=lambda s=self, img=i: \
                    s.getImg(img)).place(relx=xpos, rely=0.99, anchor=S)
            xpos = xpos + 0.08
            self.images.append(images[i])

        Button(self.frame, text='Done', command=self.exit,
               bg='red', fg='yellow').place(relx=0.99, rely=0.99, anchor=SE)
        self.frame.pack()
        self.getImg(0)

    def getImg(self, img):
        self.masterImg = Image.open(os.path.join("./images",
                                                 self.images[img]))
        self.masterImg.thumbnail((400, 400))
        self.img = ImageTk.PhotoImage(self.masterImg)
        self.lbl['image'] = self.img

    def exit(self):
        self.master.destroy()

    def selectFunc(self, tag):
        pass


root = Tk()
root.option_add('*font', ('verdana', 10, 'bold'))
root.title('Scrapbook')
scrapbook = Scrapbook(root)
root.mainloop()
