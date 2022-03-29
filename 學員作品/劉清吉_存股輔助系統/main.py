#!/usr/bin/python3.10
import threading
from models import UpdateData
from windows import Window

if __name__=="__main__":
    data = UpdateData()
    thread = threading.Thread(target=data.createDatabase)
    thread.start()

    window = Window()
    window.title("存股輔助系統")
    window.mainloop()

    thread.join()
    print("資料更新完成")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
