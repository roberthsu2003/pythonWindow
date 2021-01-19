from tkinter import *

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('Button Styles')
        for bdw in range(5):
            setattr(self, 'of%d' % bdw, Frame(self.root, borderwidth=0))
            Label(getattr(self, 'of%d' % bdw),
                  text='borderwidth = %d  ' % bdw).pack(side=LEFT)
            for relief in [RAISED, SUNKEN, FLAT, RIDGE, GROOVE, SOLID]:
                Button(getattr(self, 'of%d' % bdw), text=relief, borderwidth=bdw,
                       relief=relief, width=10,
                       command=lambda s=self, r=relief, b=bdw: s.prt(r,b))\
                          .pack(side=LEFT, padx=7-bdw, pady=7-bdw)
            getattr(self, 'of%d' % bdw).pack()

    def prt(self, relief, border):
        print('%s:%d' % (relief, border))

myGUI = GUI()
myGUI.root.mainloop()
