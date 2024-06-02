## 在 Python 中使用 Tkinter 和 ttk 模組，可以自定義應用程式的風格和主題。
- ### `以下是如何設定和使用 ttk 的 Style 和 Theme，以顯示繁體中文的簡單指南。`

### 步驟一：導入必要的模組


首先，確保導入 `tkinter` 和 `ttk` 模組：

```python
import tkinter as tk
from tkinter import ttk
```


### 步驟二：建立主應用程式視窗


創建一個主視窗，並設定標題：

```python
root = tk.Tk()
root.title("範例應用程式")
```


### 步驟三：設定繁體中文


設置 Tkinter 使用繁體中文。這通常與系統的區域設置相關，但可以手動設置字體來顯示繁體中文：

```python
# 設定預設字體
root.option_add("*Font", "微軟正黑體 12")
```


### 步驟四：設定 ttk 的 Style 和 Theme


創建並設定一個 Style 物件：

```python
style = ttk.Style()

# 列出所有可用主題
print(style.theme_names())

# 設定主題
style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' 等主題可選

# 自定義樣式
style.configure('TButton', font=('微軟正黑體', 12, 'bold'), foreground='blue')
style.configure('TLabel', font=('微軟正黑體', 12))
```


### 步驟五：建立和配置小部件


創建一些 ttk 小部件並應用自定義的樣式：

```python
# 標籤
label = ttk.Label(root, text="這是一個標籤")
label.pack(pady=10)

# 按鈕
button = ttk.Button(root, text="按鈕")
button.pack(pady=10)
```


### 完整示例程式碼


以下是完整的範例程式碼，展示如何使用 ttk 的 Style 和 Theme，並顯示繁體中文：

```python
import tkinter as tk
from tkinter import ttk

# 創建主視窗
root = tk.Tk()
root.title("範例應用程式")

# 設定預設字體
root.option_add("*Font", "微軟正黑體 12")

# 創建並設定Style
style = ttk.Style()

# 列出所有可用主題
print(style.theme_names())

# 設定主題
style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' 等主題可選

# 自定義樣式
style.configure('TButton', font=('微軟正黑體', 12, 'bold'), foreground='blue')
style.configure('TLabel', font=('微軟正黑體', 12))

# 創建標籤和按鈕
label = ttk.Label(root, text="這是一個標籤")
label.pack(pady=10)

button = ttk.Button(root, text="按鈕")
button.pack(pady=10)

# 進入主循環
root.mainloop()
```


這個範例程式碼創建了一個簡單的 GUI 應用程式，並應用了 `ttk.Style` 來設置字體和顏色，確保界面顯示繁體中文。您可以根據需要進一步調整和擴展這些樣式和設定

## 下載和套用ttkthemes提供的外觀

要下載和套用外部的主題到Tkinter，你可以使用第三方庫如`ttkthemes`來簡化這個過程。以下是具體步驟：

1. **安裝`ttkthemes`**：
   
   使用`pip`來安裝`ttkthemes`：
   ```sh
   pip install ttkthemes
   ```

2. **使用`ttkthemes`來套用主題**：

   以下是如何在你的Tkinter應用程式中使用`ttkthemes`來套用主題的範例程式碼：

   ```python
   import tkinter as tk
   from ttkthemes import ThemedTk
   from tkinter import ttk

   # 創建主窗口，使用ThemedTk替代普通的Tk
   root = ThemedTk(theme="breeze")

   # 創建一個標籤和按鈕
   label = ttk.Label(root, text="Hello, Tkinter!")
   label.pack(pady=20)

   button = ttk.Button(root, text="Click Me")
   button.pack(pady=20)

   # 開始主事件循環
   root.mainloop()
   ```

   在這個範例中，我們使用`ThemedTk`來創建主窗口並套用名為`"breeze"`的主題。你可以將`"breeze"`替換為`ttkthemes`提供的其他主題名稱。

3. **查看可用的主題**：

   如果你想查看有哪些主題可用，你可以使用以下程式碼來列出：

   ```python
   from ttkthemes import ThemedTk

   root = ThemedTk()
   print(root.get_themes())  # 列出所有可用的主題
   root.destroy()
   ```

   這段程式碼會列出`ttkthemes`庫中所有可用的主題名稱，你可以根據這些名稱來選擇你想要使用的主題。

這樣，你就可以很容易地在Tkinter應用程式中下載和套用外部的主題。