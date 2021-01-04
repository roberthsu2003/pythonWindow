# 版面
- Pack
- Grid
- Place
## Packer

```python
#lesson2_1

import tkinter as tk
from tkinter import Button
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_1")

        Button(self, text='Left').pack(side=LEFT)
        Button(self, text='Center').pack(side=LEFT)
        Button(self, text='Right').pack(side=LEFT)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic1.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_2")

        Button(self, text='Left').pack(side=LEFT)
        Button(self, text='This is th Center button').pack(side=LEFT)
        Button(self, text='Right').pack(side=LEFT)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic2.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_3")

        Button(self, text='Top').pack(side=TOP)
        Button(self, text='This is th Center button').pack(side=TOP)
        Button(self, text='Bottom').pack(side=TOP)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic3.png)	

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_4")

        fm = Frame(self)
        Button(self, text='Left').pack(side=TOP)
        Button(self, text='Center').pack(side=LEFT)
        Button(self, text='Right').pack(side=LEFT)
        fm.pack()

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic4.png)	

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_5")

        fm = Frame(self,width=300, height=200)
        Button(self, text='Left').pack(side=LEFT)
        Button(self, text='Center').pack(side=LEFT)
        Button(self, text='Right').pack(side=LEFT)
        fm.pack()

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic5.png)	

---

## 使用expand

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_6")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Left').pack(side=LEFT)
        Button(self, text='Center').pack(side=LEFT)
        Button(self, text='Right').pack(side=LEFT)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic6.png)	

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_7")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Left').pack(side=LEFT, expand=YES)
        Button(self, text='Center').pack(side=LEFT, expand=YES)
        Button(self, text='Right').pack(side=LEFT, expand=YES)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic7.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_8")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Top').pack(side=TOP, expand=YES)
        Button(self, text='Center').pack(side=TOP, expand=YES)
        Button(self, text='Bottom').pack(side=TOP, expand=YES)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```	

![](./images/pic8.png)

---

## 使用fill

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_9")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Left').pack(side=LEFT, expand=YES,fill=X)
        Button(self, text='Center').pack(side=LEFT, expand=YES,fill=X)
        Button(self, text='Right').pack(side=LEFT, expand=YES,fill=X)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic9.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_10")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Top').pack(side=TOP, fill=X)
        Button(self, text='Center').pack(side=TOP, fill=X)
        Button(self, text='Bottom').pack(side=TOP, fill=X)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic10.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_11")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Left').pack(side=LEFT, expand=NO,fill=X)
        Button(self, text='Center').pack(side=LEFT, expand=NO,fill=X)
        Button(self, text='Right').pack(side=LEFT, expand=YES,fill=X)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic11.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_12")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Left').pack(side=TOP, expand=YES,fill=X)
        Button(self, text='Center').pack(side=TOP, expand=YES,fill=X)
        Button(self, text='Right').pack(side=TOP, expand=YES,fill=X)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic12.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_13")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Left').pack(side=LEFT, expand=YES,fill=BOTH)
        Button(self, text='Center').pack(side=LEFT, expand=YES,fill=BOTH)
        Button(self, text='Right').pack(side=LEFT, expand=YES,fill=BOTH)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic13.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_14")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='TOP').pack(side=TOP, expand=YES,fill=BOTH)
        Button(self, text='Center').pack(side=TOP, expand=YES,fill=BOTH)
        Button(self, text='Bottom').pack(side=TOP, expand=YES,fill=BOTH)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic14.png)

---

## 使用padx和pady

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_15")

        fm = Frame(self,width=300, height=200)
        Button(self, text='Left').pack(side=LEFT)
        Button(self, text='Center').pack(side=LEFT, padx=10)
        Button(self, text='Right').pack(side=LEFT)
        fm.pack()

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic15.png)

---

## 使用anchor

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_16")
        self.geometry("300x200")
        fm = Frame(self)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic16.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_17")
        self.geometry("300x200")
        fm = Frame(self)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic17.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_18")

        fm = Frame(self)
        Button(fm, text='TOP').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='CENTER').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='Bottom').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='LEFT').pack(side=LEFT)
        Button(fm, text='This is Center Button').pack(side=LEFT)
        Button(fm, text='Right').pack(side=LEFT)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic18.png)

---

```python
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_19")

        fm = Frame(self)
        Button(fm, text='TOP').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='CENTER').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='Bottom').pack(side=TOP,expand=YES, anchor=W,fill=X)
        fm.pack(side=LEFT, fill=BOTH, expand=YES)

        fm1 = Frame(self)
        Button(fm1, text='LEFT').pack(side=LEFT)
        Button(fm1, text='This is Center Button').pack(side=LEFT)
        Button(fm1, text='Right').pack(side=LEFT)
        fm1.pack(side=LEFT, padx=10)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
```

![](./images/pic19.png)

---










