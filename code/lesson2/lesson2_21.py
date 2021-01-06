from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import sys, Pmw


class Enhancer:
    def __init__(self, master=None, imgfile=None):
        self.master = master
        self.masterImg = Image.open(imgfile)
        self.masterImg.thumbnail((150, 150))

        for i in range(9):
            image = self.masterImg.copy()
            setattr(self, 'image%d' % i, image)
            setattr(self, 'img%d' % i, ImageTk.PhotoImage(image.mode,
                                                          image.size))
        i = 0
        for r in range(3):
            for c in range(3):
                lbl = Label(master, image=getattr(self, 'img%d' % i))
                setattr(self, 'lbl%d' % i, lbl)
                getattr(self, 'lbl%d' % i).grid(row=r * 5, column=c * 2,
                                                rowspan=5, columnspan=2,
                                                sticky=W + E + S + N, padx=5, pady=5)
                i = i + 1

        self.original = ImageTk.PhotoImage(self.masterImg)
        Label(master, image=self.original).grid(row=0, column=6,
                                                rowspan=5, columnspan=2)

        Label(master, text='Enhance', bg='gray70').grid(row=5, column=6,
                                                        columnspan=2, sticky=N + S + W + E)
        self.radio = Pmw.RadioSelect(master, labelpos=None,
                                     buttontype='radiobutton', orient='vertical',
                                     command=self.selectFunc)
        self.radio.grid(row=6, column=6, rowspan=4, columnspan=2)

        self.varFactor = 0.2
        self.enh = {}
        for lbl, enh in (('Focus', ImageEnhance.Sharpness),
                         ('Contrast', ImageEnhance.Contrast),
                         ('Brightness', ImageEnhance.Brightness),
                         ('Color', ImageEnhance.Color)):
            self.radio.add(lbl)
            self.enh[lbl] = enh
        self.radio.invoke('Color')
        self.currentEnh = self.enh['Color']

        Label(master, text='Variation', bg='gray70').grid(row=10, column=6,
                                                          columnspan=2, sticky=N + S + W + E)

        self.variation = Pmw.ComboBox(master, history=0, entry_width=11,
                                      selectioncommand=self.setVariation,
                                      scrolledlist_items=('Fine', 'Medium Fine', 'Medium',
                                                          'Medium Course', 'Course'))
        self.variation.selectitem('Medium')
        self.variation.grid(row=11, column=6, columnspan=2)

        Button(master, text='Undo', state='disabled').grid(row=13, column=6)
        Button(master, text='Apply', state='disabled').grid(row=13, column=7)
        Button(master, text='Reset', state='disabled').grid(row=14, column=6)
        Button(master, text='Done', command=self.exit).grid(row=14, column=7)

    def exit(self):
        self.master.destroy()

    def selectFunc(self, tag):
        self.currentEnh = self.enh[tag]
        self.doEnhancement()

    def setVariation(self, tag):
        self.varFactor = {'Fine': 0.05, 'Medium Fine': 0.1,
                          'Medium': 0.2, 'Medium Course': 0.3,
                          'Course': 0.5}[tag]
        self.doEnhancement()

    def doEnhancement(self):
        values = []
        for i in range(5):
            values.append(1.0 - (i * self.varFactor))
        values.reverse()
        for i in range(4):
            values.append(1.0 + ((i + 1) * self.varFactor))

        i = 0
        for v in values:
            enhancer = self.currentEnh(getattr(self, 'image%d' % i))
            getattr(self, 'img%d' % i).paste(enhancer.enhance(v))
            i = i + 1


root = Tk()
root.option_add('*font', ('verdana', 10, 'bold'))
root.title('Image Enhancement')
imgEnh = Enhancer(root, sys.argv[1])
root.mainloop()