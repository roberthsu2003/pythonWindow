import tkinter as tk
from parts import TopFrame,MedianFrame,BottomFrame


class Window(tk.Tk):
    
    def __init__(self):
        super().__init__()
        topFrame = TopFrame(self,borderwidth=0)       
        topFrame.pack()        
        medianFrame = MedianFrame(self,borderwidth=0)
        medianFrame.pack(fill=tk.X)
        bottomFrame = BottomFrame(self)
        bottomFrame.pack(fill=tk.X)

    def radioButtonEventOfMedianFrame(self,radioButtonValue):
        print(radioButtonValue)

    def listBoxEventOfBottomFrame(self,listBoxValue):
        print(listBoxValue)

    def comboBoxEventOfBottomFrame(self,comboValue):
        print(comboValue)

        
        

def main():
    window = Window()
    window.title("Widgets")
    window.mainloop()

if __name__ == "__main__":
    main()