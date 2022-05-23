#! usr/bin/python3.10
def func1():
    func2()
    print("這是func1")

def func2():
    func3()
    print("這是func2")

def func3():
    print("這是func3")

if __name__ == "__main__":
    print("這是主程式")
    func1()
    print("程式結束")