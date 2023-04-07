import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class TopFrame(ttk.LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        #using ttk.Style to change the style of the self widget
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('default')
        #ttkStyle change ttk.LabelFrame border width
        ttkStyle.configure('TLabelframe',borderwidth=0)
        flowerImage1 = Image.open("./images/flower1.png")
        self.flowerPhoto1 = ImageTk.PhotoImage(flowerImage1)
        self.canvas = tk.Canvas(self, width=173, height=200)
        self.canvas.pack()
        self.canvas.create_image(0,5,image=self.flowerPhoto1,anchor='nw')
        self.canvas.create_text(0,200,text='Flower', fill='yellow', font=('verdana', 36),
        anchor='sw')

        diamondImage1 = Image.open("./images/diamond.png")
        self.diamondPhoto1 = ImageTk.PhotoImage(diamondImage1)
        self.canvas.create_image(175,5,image=self.diamondPhoto1,anchor='nw')

        atomImage1 = Image.open("./images/atom.png")
        self.atomPhoto1 = ImageTk.PhotoImage(atomImage1)
        self.canvas.create_image(280,5,image=self.atomPhoto1,anchor='nw')

        #created ttk.scrollbar of tkinter in canvas
        self.scrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scrollbar.pack(side='bottom', fill='x')
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.configure(scrollregion=(0,0,500,200))


class MedianFrame(ttk.LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        # create ttk.radiobuttons in self
        # ttk.Style change ttk.Radiobutton shape
        self.w = master
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('clam')          
        radionFrame = ttk.LabelFrame(self, text='Radio Buttons')
        radionFrame.pack(side=tk.LEFT, padx=10, pady=10)
        self.radioStringVar = tk.StringVar()
        self.radiobutton1 = ttk.Radiobutton(radionFrame, text='Option 1',variable=self.radioStringVar,value="red",command=self.radioEvent)
        self.radiobutton1.pack()
        self.radiobutton2 = ttk.Radiobutton(radionFrame, text='Option 2',variable=self.radioStringVar,value="blue",command=self.radioEvent)
        self.radiobutton2.pack()
        self.radiobutton3 = ttk.Radiobutton(radionFrame, text='Option 3', variable=self.radioStringVar,value="green",command=self.radioEvent)
        self.radiobutton3.pack()
        self.radiobutton4 = ttk.Radiobutton(radionFrame, text='Option 4', variable=self.radioStringVar,value="yellow",command=self.radioEvent)
        self.radiobutton4.pack()
        self.radioStringVar.set('red')

        # create ttk.checkbuttons in self
        checkFrames = ttk.LabelFrame(self, text='Check Buttons')
        checkFrames.pack(side=tk.RIGHT, padx=10, pady=10)

        self.checkStringVar1 = tk.StringVar()
        self.checkStringVar2 = tk.StringVar()
        self.checkStringVar3 = tk.StringVar()
        self.checkStringVar4 = tk.StringVar()

        self.checkbutton1 = ttk.Checkbutton(checkFrames, text='Option 1',variable=self.checkStringVar1,command=self.checkEvent,onvalue='op1check',offvalue='op1off')
        self.checkbutton1.pack()
        self.checkbutton2 = ttk.Checkbutton(checkFrames, text='Option 2',variable=self.checkStringVar2,command=self.checkEvent,onvalue='op2check',offvalue='op2off')
        self.checkbutton2.pack()
        self.checkbutton3 = ttk.Checkbutton(checkFrames, text='Option 3', variable=self.checkStringVar3,command=self.checkEvent,onvalue='op3check',offvalue='op3off')
        self.checkbutton3.pack()
        self.checkbutton4 = ttk.Checkbutton(checkFrames, text='Option 4', variable=self.checkStringVar4,command=self.checkEvent,onvalue='op4check',offvalue='op4off')
        self.checkbutton4.pack() 
        
    
    def radioEvent(self):
        self.w.radioButtonEventOfMedianFrame(self.radioStringVar.get())

    def checkEvent(self):
        print(self.checkStringVar1.get())
        print(self.checkStringVar2.get())
        print(self.checkStringVar3.get())
        print(self.checkStringVar4.get())
        #self.w.radioButtonEventOfMedianFrame(self.checkStringVar.get())


class BottomFrame(ttk.LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        listFrame = ttk.LabelFrame(self,text="List Box")
        listFrame.pack(side=tk.LEFT,padx=10,pady=10) 
        list = tk.Listbox(listFrame,height=6,width=10)
        list.pack(side=tk.LEFT)
        for month in range(1,13):
            list.insert(tk.END,f"{month}月")

        scrollBar = ttk.Scrollbar(listFrame,command=list.yview)
        scrollBar.pack(side=tk.RIGHT,fill=tk.Y)
        list.configure(yscrollcommand=scrollBar.set)

    






