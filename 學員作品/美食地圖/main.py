import tkinter as tk
from tkinter import ttk
from search import search_places
import googlemaps
import requests
from io import BytesIO
from tkinter import Tk, Button, PhotoImage
from tkinter import Tk, Button, messagebox
import io
from PIL import Image, ImageTk
import webbrowser

API_KEY = 'AIzaSyCJxyreN2bQmxOgYTLL-BqcAVXNnA714jY'
gmaps = googlemaps.Client(key=API_KEY)

# 每頁呈現的結果數量
display_count = 10

def show_results():
    global start, page, total_pages
    
    tree.delete(*tree.get_children())
    for i in range(start, start + display_count):
        if i >= len(results):
            break
        result = results[i]
        tree.insert("", tk.END, values=(result['name'], result['address'], result['rating']))
    
    pages_label.config(text=f"第 {page+1} 頁 / 共 {total_pages} 頁")

def search():
    global results, start, page, total_pages
    
    area = entry.get()
    results = search_places(area)
    start = 0
    page = 0
    total_pages = (len(results) - 1) // display_count + 1
    show_results()


def show_map():
    selection = tree.selection()
    if selection:
        item = tree.item(selection[0])
        name = item['values'][0]
        for result in results:
            if result['name'] == name:
                place_id = result['place_id']
                place = gmaps.place(place_id, language='zh-TW', fields=['name', 'formatted_address', 'rating', 'photo'])['result']
                name = place['name']
                address = place['formatted_address']
                rating = place.get('rating', None)
                photo_reference = place.get('photos', [])[0].get('photo_reference', None)
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}" if photo_reference is not None else None
                
                # 產生 Google Maps 的查詢網址
                query = f"https://www.google.com/maps/search/?api=1&query={address}&query_place_id={place_id}"
                webbrowser.open(query)
                
                # 顯示餐廳照片和資訊
                if photo_url is not None:
                    # 讀取照片
                    response = requests.get(photo_url)
                    img = Image.open(io.BytesIO(response.content))
                    
                    # 建立小視窗
                    window = tk.Toplevel()
                    window.title(name)
                    window.geometry("660x800")
                    window.title("我的口袋名單")
                    window.resizable(False, False)

                    # 創建主選單
                    menubar = tk.Menu(window)
                    window.config(menu=menubar)

                    # 創建操作選單
                    operations_menu = tk.Menu(menubar, tearoff=0)
                    menubar.add_cascade(label='操作', menu=operations_menu)

                # 創建一個空的frame來演示工具列
                    toolbar = tk.Frame(window, bg='white', height=40)
                    toolbar.pack(side=tk.TOP, fill=tk.X)
                    
                    # 顯示照片
                    img_tk = ImageTk.PhotoImage(img)
                    label_photo = tk.Label(window, image=img_tk)
                    label_photo.pack()

                    # 顯示餐廳資訊
                    frame_info = tk.Frame(window)
                    frame_info.pack(pady=10)
                    
                    label_name = tk.Label(frame_info, text=name, font=('Arial', 16, 'bold'))
                    label_name.grid(row=0, column=0, columnspan=2, sticky='w')
                    
                    label_address_title = tk.Label(frame_info, text='地址：', font=('Arial', 12))
                    label_address_title.grid(row=1, column=0, sticky='e')
                    label_address_value = tk.Label(frame_info, text=address, font=('Arial', 12))
                    label_address_value.grid(row=1, column=1, sticky='w')
                    
                    label_rating_title = tk.Label(frame_info, text='評分：', font=('Arial', 12))
                    label_rating_title.grid(row=2, column=0, sticky='e')
                    label_rating_value = tk.Label(frame_info, text=rating, font=('Arial', 12))
                    label_rating_value.grid(row=2, column=1, sticky='w')

                    # 新增加入口袋名單的選項
                    # 新增一個口袋名單的 Treeview
                    pocket_tree = ttk.Treeview(window)
                    pocket_tree.pack(pady=10)

                    # 新增口袋名單的欄位
                    pocket_tree['columns'] = ('name', 'address', 'rating')
                    pocket_tree.column('#0', width=0, stretch=tk.NO)
                    pocket_tree.column('name', width=150, anchor='w')
                    pocket_tree.column('address', width=250, anchor='w')
                    pocket_tree.column('rating', width=100, anchor='w')

                    # 設定欄位名稱
                    pocket_tree.heading('#0', text='', anchor='w')
                    pocket_tree.heading('name', text='餐廳名稱', anchor='w')
                    pocket_tree.heading('address', text='地址', anchor='w')
                    pocket_tree.heading('rating', text='評分', anchor='w')

                    # 新增選定餐廳到口袋名單的函數
                    def add_to_pocket():
                        selected_restaurant = {'name': name, 'address': address}
                        pocket_tree.insert('', 'end', values=(selected_restaurant['name'], selected_restaurant['address']))
                        messagebox('已加入口袋名單')

                    operations_menu.add_command(label='加入口袋名單', command=add_to_pocket)

                    # 新增返回選項
                    def go_back():
                        print('返回')
                    operations_menu.add_command(label='返回', command=go_back)
                    
                    # 在frame上新增一個菜單按鈕
                    menu_button1 = tk.Menubutton(toolbar, text='追蹤店家', relief='raised', direction='below')
                    menu_button1.pack(side=tk.LEFT, padx=5, pady=5)

                    # 設置菜單按鈕的選單為操作選單
                    menu_button1.config(menu=operations_menu)

                    window.mainloop()
                break
    else:
        messagebox.showinfo("操作錯誤", "您尚未選擇任何一間店家唷!")


def next_page():
    global page, start
    if page < total_pages - 1:
        page += 1
        start += display_count
        show_results()

def prev_page():
    global page, start
    if page > 0:
        page -= 1
        start -= display_count
        show_results()

window = tk.Tk()
window.geometry("900x800")
window.title("餐廳搜尋系統")
window.resizable(False, False)

# 載入圖片
background_image = tk.PhotoImage(file="food04.png")

# 將圖片設定為視窗背景
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

style = ttk.Style(window)
style.theme_use("clam")
style.configure(".", font=("Helvetica", 12))
style.configure("TLabel", foreground="#1D3607", background="#EFECE4")
style.configure("TButton", foreground="white", background="#385D8D")
style.map("TButton", background=[("active", "#768CA9")])


image = tk.PhotoImage(file="icon.png")
window.iconphoto(False, image)

label = ttk.Label(window, text="搜 尋 關 鍵 字", font= ("Times New Roman", 18, "bold"))
label.pack(pady=10)

entry = ttk.Entry(window, width=20, font=("Times New Roman", 16))
entry.pack(pady=10)

button = ttk.Button(window, text="搜尋",command=search)
button.pack(pady=10)

frame = ttk.Frame(window)
frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame, columns=("Name", "Address", "Rating"), show="headings")
tree.heading("Name", text="店名")
tree.heading("Address", text="地址")
tree.heading("Rating", text="評分")
tree.column("Name", width=200)
tree.column("Address", width=400)
tree.column("Rating", width=50)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.configure(yscrollcommand=scrollbar.set)

pages_label = ttk.Label(window, text="")
pages_label.pack(pady=10)

# 創建 Frame
button_frame = ttk.Frame(window)

# 加載圖片
image = PhotoImage(file="box1.png")

#打開地圖查看鈕:
map_button = tk.Button(window, image=image, command=lambda: show_map())
map_button.pack(anchor=tk.CENTER)

# 將按鈕放置在 Frame 中
map_button.pack(anchor="center")

# 創建上一頁按鈕並設置回調函數
prev_button = ttk.Button(button_frame, text="上一頁", command=prev_page)
prev_button.pack(side="left", padx=10)

# 創建下一頁按鈕並設置回調函數
next_button = ttk.Button(button_frame, text="下一頁", command=next_page)
next_button.pack(side="right", padx=10)

# 將 Frame 放置在視窗中
button_frame.pack(anchor="n", pady=10)

window.mainloop()