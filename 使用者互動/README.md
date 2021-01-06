# 使用者互動

	GUI的應用程式，大量依靠和使用者的互動，而這些互動全部建立於事件和回呼。說簡單一點，就是讓工具附加上功能。

## 事件導向系統

	tkinter 內部有事件機制，只要了解工具如何綁定事件，將可以輕鬆和使用者達成互動。每個工具都有一個bind()方法，使用bind()方法就可以綁定事件

```python
from tkinter import *

root = Tk()

def enter(event):
    print('Entered Frame: x=%d, y=%d' % (event.x, event.y))

frame = Frame(root, width=150, height=150)
frame.bind('<Any-Enter>', enter)
frame.pack()

root.mainloop()
```

## tkinter事件
### 事件
語法:使用字串格式
<modifier-type-qualifier>
- <Any-Enter>
- <Button-1>
- <Button-2>
- <B2-Motion>
- <ButtonRelease-3>
- <Configure>
- <Control-Insert>
- <Control-Shift-F3>
- <Destroy>
- <Double-Button-1>
- <Enter>
- <FocusIn>
- <FocusOut>
- <KeyPress>
- <KeyRelease-back-slash>
- <Leave>
- <Print>

```python
frame.bind('<Any-Enter>', enter)
```

### 回呼函式
- 最直接也是最簡單的方式
- 使用command屬性

```python
btn = Button(frame, text='OK', command=buttonAction)

def buttonAction(event=None):
	if event:
		print('event in: %s' % event.type)
	else:
		print('command in')
```

上面的建立的回呼方式和下面綁定效果是一樣的

```python
btn.bind('<Button-1>', buttonAction)
btn.bind('<KeyPress-space>', buttonAction)
```

