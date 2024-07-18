#自定義module
import windows
from windows import Window

def main():

    #視窗建立
    def on_closing():
        window.destroy()
        window.quit()

    window = Window(theme="arc")
    window.protocol("WM_DELETE_WINDOW",on_closing)
    window.mainloop()


if __name__ =="__main__":
    main()