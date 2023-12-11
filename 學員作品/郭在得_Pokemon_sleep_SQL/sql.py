import sqlite3
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk

# 主介面
class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.conn=sqlite3.connect("pokemon_database.db")

        # 標題----------------------------------------------
        topFrame=tk.Frame(self,relief=tk.GROOVE)
        tk.Label(topFrame,text="Pokemon Sleep SQL",font=("arial",20,"bold")).pack(padx=20,pady=(20,0),side=LEFT)
        topFrame.pack()

        # 新增按鈕-------------------------------------------
        self.b=ttk.Button(self,text="新增神奇寶貝",bootstyle=WARNING,command=self.open_NewPokemon)
        self.b.place(x=10,y=90)

        # 搜尋-----------------------------------------------
        self.search_box = ttk.LabelFrame(text="搜尋",bootstyle=DANGER)
        self.search_box.pack(fill="x",padx=(120,10),pady=10)

        # 名字
        tk.Label(self.search_box, text="名稱：").pack(side=LEFT)
        self.search_name= ttk.Entry(self.search_box,bootstyle=DANGER)
        self.search_name.bind("<KeyRelease>",self.get_search_name)
        self.search_name.pack(side="left",pady=10)

        # 食材
        self.i = tk.StringVar()
        self.i.set("食材類型")
        ingredient_type = ttk.Menubutton(self.search_box,bootstyle=(OUTLINE,DANGER))
        ingredient_type["textvariable"] = self.i
        self.ingredient_type_values = ("食材類型",'01 粗枝大蔥','02 品鮮蘑菇','03 特選蛋','04 窩心洋芋','05 特選蘋果',
                                  '06 火辣香草','07 豆製肉','08 哞哞鮮奶','09 甜甜蜜','10 純粹油',
                                  '11 暖暖薑','12 好眠番茄','13 放鬆可可','14 美味尾巴','15 萌綠大豆')
        ingredient_type_menu = tk.Menu(ingredient_type, tearoff=0)
        for ingredient in self.ingredient_type_values:
            ingredient_type_menu.add_command(
                label=ingredient, 
                command=lambda val=ingredient: self.i.set(val),
                activebackground="pink"
            )
        ingredient_type["menu"] = ingredient_type_menu
        self.i.trace('w', self.get_search_name)
        ingredient_type.pack(padx=10,pady=10, side=tk.RIGHT)

        # 樹果類型
        self.f = tk.StringVar()
        self.f.set("樹果類型")
        fruit_type = ttk.Menubutton(self.search_box,bootstyle=DANGER)
        fruit_type["textvariable"] = self.f
        self.fruit_type_values = ('樹果類型','01 柿仔果', '02 蘋野果','03 橙橙果','04 萄葡果','05 金枕果',
                             '06 莓莓果','07 櫻子果','08 零餘果','09 勿花果','10 椰木果',
                             '11 芒芒果','12 木子果','13 文柚果','14 墨莓果','15 番荔果',
                             '16 異奇果','17 靛莓果','18 桃桃果')
        fruit_type_menu = tk.Menu(fruit_type, tearoff=0)
        for fruit in self.fruit_type_values:
            fruit_type_menu.add_command(
                label=fruit, 
                command=lambda val=fruit: self.f.set(val),
                activebackground="pink"
            )
        fruit_type["menu"] = fruit_type_menu
        self.f.trace('w', self.get_search_name)
        fruit_type.pack(padx=10,pady=10, side=tk.RIGHT)

        #tree view-----------------------------------------------------
        self.treeview=tk.Frame(self)
        self.pokemon_data=PokemonTreeView(self.treeview,show="headings",
        columns=('id','name','help_fruit','help_ingredient_1'),height=20)
        self.pokemon_data.pack(side=LEFT,padx=10,pady=10)

        # 捲動軸
        scroll=ttk.Scrollbar(self.treeview,orient="vertical",command=self.pokemon_data.yview,bootstyle=PRIMARY)
        scroll.pack(side=LEFT,fill="y")
        self.pokemon_data.configure(yscrollcommand=scroll.set)
        self.treeview.pack(pady=(0,30),padx=20,expand=True,fill="x")

        # 放大顯示名稱----------------------------------------------
        self.display_name=ttk.Label(font=("arial",20,"bold"),bootstyle=PRIMARY)
        self.display_name.place(x=310,y=160)

        # 圓圈圈-----------------------------------------------------
        self.meter=ttk.Meter(
            metersize=200,
            padding=5,
            amountused=0,
            amounttotal=2000,
            metertype="full",
            subtext="SP值",
            interactive=FALSE,
            stripethickness=2
        )
        self.meter.place(x=325,y=220)

        # 能力詳情--------------------------------------------------
        self.display_power_up=ttk.Label(font=("arial",12,"bold"),bootstyle=PRIMARY)
        self.display_power_up.place(x=310,y=435)

        self.display_power_down=ttk.Label(font=("arial",12,"bold"),bootstyle=PRIMARY)
        self.display_power_down.place(x=310,y=465)

        # 绑定treeview的<<TreeviewSelect>>事件到更新函數
        self.pokemon_data.bind("<<TreeviewSelect>>", self.update_right)

    # 更新數值
    def update_right(self, *args):
        selected_item = self.pokemon_data.selection()
        id = self.pokemon_data.item(selected_item)['values'][0]
        sp_value, power_up, power_down, img_num = self.get_pokemon_data(id)

        # 更新 meter
        self.meter.configure(amountused=sp_value)

        # 更新 display_name
        name = self.pokemon_data.item(selected_item)['values'][1]
        self.display_name.configure(text=f"{name}")

        # 更新 display_power_up
        self.display_power_up.configure(text=f"{power_up}  ▲ ▲")

        # 更新 display_power_down
        self.display_power_down.configure(text=f"{power_down}  ▼ ▼")

        # 更新圖片
        if hasattr(self, 'jpg') and isinstance(self.jpg, tk.Toplevel):
            self.jpg.destroy()
        self.show_image(img_num)

    # 從database裡獲取資料 for更新數值
    def get_pokemon_data(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT sp, power_up, power_down,img_num FROM pokemon WHERE id={id}")
        result = cursor.fetchone()
        if result:
            sp_value, power_up, power_down, img_num = result
            return sp_value, power_up, power_down, img_num
    
    # 顯示神奇寶貝圖片
    def show_image(self, img_num):
        img_path = f'display_data/{img_num}.jpg'

        try:
            img = Image.open(img_path)
            tk_img = ImageTk.PhotoImage(img)

            x_pos = self.winfo_x() + self.winfo_width()+10
            y_pos = self.winfo_y()+200

            self.jpg = tk.Toplevel()
            self.jpg.title(f"神奇寶貝-編號{img_num}")
            self.jpg.geometry(f'+{x_pos}+{y_pos}')

            label = tk.Label(self.jpg, image=tk_img)
            label.image = tk_img 
            label.pack()
        except FileNotFoundError:
            print(f"Image {img_num}.jpg not found")
    
    # 把search_name引入treeview
    def get_search_name(self, *args):
        text = self.search_name.get().lower()
        fruit = self.f.get()
        ingredient = self.i.get()

        conditions = []
        if text:
            conditions.append(f"SELECT * FROM pokemon WHERE name LIKE '%{text}%'")
        if fruit and fruit != '樹果類型':
            conditions.append(f" SELECT * FROM pokemon WHERE help_fruit = '{fruit}'")
        if ingredient and ingredient != '食材類型':
            conditions.append(f" SELECT * FROM pokemon WHERE help_ingredient_1 = '{ingredient}'")

        where_clause = " ".join(conditions)
        if where_clause:
            sql=where_clause
            self.data = pd.read_sql_query(sql, self.conn)
            self.pokemon_data.display_data(self.data)

    # 打開NewPokemon視窗
    def open_NewPokemon(self):
        open_window=NewPokemon()
        open_window.title("新增神奇寶貝")
        open_window.resizable(width=False,height=False)
        open_window.mainloop()

# 新增神奇寶貝介面
class NewPokemon(tk.Toplevel):
    def __init__(self,event=None,**kwargs):
        super().__init__(event,**kwargs)
        self.pokemon_data={}

        # 標題----------------------------------------------
        topFrame=tk.Frame(self,relief=tk.GROOVE)
        tk.Label(topFrame,text="新增神奇寶貝",font=("arial",20,"bold")).pack(padx=20,pady=(20,0),side=tk.LEFT)
        topFrame.pack()

        # 基本資料---------------------------------------
        search_box = ttk.LabelFrame(self,text="基本資料",bootstyle=WARNING)
        search_box.pack(fill="x",padx=(10,10),pady=10)

        # 編號
        tk.Label(search_box, text="編號：").pack(side=tk.LEFT)
        self.img_num= ttk.Entry(search_box,bootstyle=WARNING,width=5)
        self.img_num.pack(side="left",pady=10)

        # 名字
        tk.Label(search_box, text="名稱：").pack(side=LEFT)
        self.name= ttk.Entry(search_box,bootstyle=WARNING)
        self.name.pack(side="left",pady=10)

        # sp
        tk.Label(search_box, text="SP值").pack(side=LEFT)
        self.sp= ttk.Entry(search_box,bootstyle=WARNING,width=5)
        self.sp.pack(side="left",pady=10)

        # 專長
        self.expertise = tk.StringVar()
        self.expertise.set("專長")
        expertise = ttk.Menubutton(search_box,bootstyle=(OUTLINE,WARNING))
        expertise["textvariable"] = self.expertise
        expertise_values = ('樹果','食材','技能')
        expertise_menu = tk.Menu(expertise, tearoff=0)
        for ex in expertise_values:
            expertise_menu.add_command(
                label=ex, 
                command=lambda val=ex: self.expertise.set(val),
                activebackground="#CDAF95"
            )
        expertise["menu"] = expertise_menu
        expertise.pack(padx=10,pady=10, side=tk.LEFT)

        # 等級
        tk.Label(search_box, text="等級：").pack(side=LEFT)
        self.level= ttk.Entry(search_box,bootstyle=WARNING,width=5)
        self.level.pack(side="left",pady=10)

        # 幫忙間隔
        tk.Label(search_box, text="幫忙間隔：").pack(side="left",padx=(50,0),pady=10)
        self.help_time = ttk.Entry(search_box, style="WARNING", width=10)
        self.help_time.pack(side="left",pady=10)

        # 持有上限
        tk.Label(search_box, text="持有上限：").pack(side="left",pady=10)
        self.help_max = ttk.Entry(search_box, style="WARNING", width=10)
        self.help_max.pack(side="left",pady=10)

        # 幫忙能力---------------------------------------
        help_box = ttk.LabelFrame(self,text="幫忙能力",bootstyle=WARNING)
        help_box.pack(fill="x",padx=(10,10),pady=10)

        # 樹果類型
        self.help_fruit = tk.StringVar()
        self.help_fruit.set("樹果類型")
        help_fruit = ttk.Menubutton(help_box,bootstyle=WARNING)
        help_fruit["textvariable"] = self.help_fruit
        help_fruit_values = ('01 柿仔果', '02 蘋野果','03 橙橙果','04 萄葡果','05 金枕果',
                             '06 莓莓果','07 櫻子果','08 零餘果','09 勿花果','10 椰木果',
                             '11 芒芒果','12 木子果','13 文柚果','14 墨莓果','15 番荔果',
                             '16 異奇果','17 靛莓果','18 桃桃果')
        self.help_fruit_menu = tk.Menu(help_fruit, tearoff=0)
        for fruit in help_fruit_values:
            self.help_fruit_menu.add_command(
                label=fruit, 
                command=lambda val=fruit: self.help_fruit.set(val),
                activebackground="#CDAF95"
            )
        help_fruit["menu"] = self.help_fruit_menu
        help_fruit.pack(padx=10,pady=10, side=tk.LEFT)

        # 樹果加成
        self.image_label = tk.Label(help_box, text="樹果加成：")
        self.image_label.pack(side=tk.LEFT)
        self.image_label.bind("<Button-1>", self.show_fruit_image)
        self.help_fruit_num_1= ttk.Entry(help_box,bootstyle=WARNING,width=5)
        self.help_fruit_num_1.pack(side="left",pady=10)

        # 食材1
        self.help_ingredient_1 = tk.StringVar()
        self.help_ingredient_1.set("食材類型1")
        help_ingredient_1 = ttk.Menubutton(help_box,bootstyle=WARNING)
        help_ingredient_1["textvariable"] = self.help_ingredient_1
        help_ingredient_1_values = ('01 粗枝大蔥','02 品鮮蘑菇','03 特選蛋','04 窩心洋芋','05 特選蘋果',
                                  '06 火辣香草','07 豆製肉','08 哞哞鮮奶','09 甜甜蜜','10 純粹油',
                                  '11 暖暖薑','12 好眠番茄','13 放鬆可可','14 美味尾巴','15 萌綠大豆')
        help_ingredient_1_menu = tk.Menu(help_ingredient_1, tearoff=0)
        for ingredient in help_ingredient_1_values:
            help_ingredient_1_menu.add_command(
                label=ingredient, 
                command=lambda val=ingredient: self.help_ingredient_1.set(val),
                activebackground="#CDAF95"
            )
        help_ingredient_1["menu"] = help_ingredient_1_menu
        help_ingredient_1.pack(padx=10,pady=10, side=tk.LEFT)

        # 食材加成1
        tk.Label(help_box, text="加成1：").pack(side=LEFT)
        self.help_ingredient_num_1= ttk.Entry(help_box,bootstyle=WARNING,width=5)
        self.help_ingredient_num_1.pack(side="left",pady=10)

        # 食材2
        self.help_ingredient_2 = tk.StringVar()
        self.help_ingredient_2.set("食材類型2")
        help_ingredient_2 = ttk.Menubutton(help_box,bootstyle=WARNING)
        help_ingredient_2["textvariable"] = self.help_ingredient_2
        help_ingredient_2_values = ('01 粗枝大蔥','02 品鮮蘑菇','03 特選蛋','04 窩心洋芋','05 特選蘋果',
                                  '06 火辣香草','07 豆製肉','08 哞哞鮮奶','09 甜甜蜜','10 純粹油',
                                  '11 暖暖薑','12 好眠番茄','13 放鬆可可','14 美味尾巴','15 萌綠大豆')
        help_ingredient_2_menu = tk.Menu(help_ingredient_2, tearoff=0)
        for ingredient in help_ingredient_2_values:
            help_ingredient_2_menu.add_command(
                label=ingredient, 
                command=lambda val=ingredient: self.help_ingredient_2.set(val),
                activebackground="#CDAF95"
            )
        help_ingredient_2["menu"] = help_ingredient_2_menu
        help_ingredient_2.pack(padx=10,pady=10, side=tk.LEFT)

        # 食材加成2
        tk.Label(help_box, text="加成2：").pack(side=LEFT)
        self.help_ingredient_num_2= ttk.Entry(help_box,bootstyle=WARNING,width=5)
        self.help_ingredient_num_2.pack(side="left",pady=10)

        # 食材3
        self.help_ingredient_3 = tk.StringVar()
        self.help_ingredient_3.set("食材類型3")
        help_ingredient_3 = ttk.Menubutton(help_box,bootstyle=WARNING)
        help_ingredient_3["textvariable"] = self.help_ingredient_3
        help_ingredient_3_values = ('01 粗枝大蔥','02 品鮮蘑菇','03 特選蛋','04 窩心洋芋','05 特選蘋果',
                                  '06 火辣香草','07 豆製肉','08 哞哞鮮奶','09 甜甜蜜','10 純粹油',
                                  '11 暖暖薑','12 好眠番茄','13 放鬆可可','14 美味尾巴','15 萌綠大豆')
        help_ingredient_3_menu = tk.Menu(help_ingredient_3, tearoff=0)
        for ingredient in help_ingredient_3_values:
            help_ingredient_3_menu.add_command(
                label=ingredient, 
                command=lambda val=ingredient: self.help_ingredient_3.set(val),
                activebackground="#CDAF95"
            )
        help_ingredient_3["menu"] = help_ingredient_3_menu
        help_ingredient_3.pack(padx=10,pady=10, side=tk.LEFT)

        # 食材加成3
        tk.Label(help_box, text="加成3：").pack(side=LEFT)
        self.help_ingredient_num_3= ttk.Entry(help_box,bootstyle=WARNING,width=5)
        self.help_ingredient_num_3.pack(side="left",padx=(0,10),pady=10)

        # 主技能 ---------------------------------------
        skill_main_box = ttk.LabelFrame(self, text="主技能 & 性格加成", style="WARNING")
        skill_main_box.pack(fill="x", padx=(10, 10), pady=10)

        self.skill_main = tk.StringVar()
        self.skill_main.set("主技能")
        skill_main = ttk.Menubutton(skill_main_box,bootstyle=(OUTLINE,WARNING))
        skill_main["textvariable"] = self.skill_main
        skill_main_values = ('能量填充','活力填充','活力療癒','活力全體療癒','夢之碎片獲取',
                             '食材獲取', '幫手支援','料理強化', '揮指')
        skill_main_menu = tk.Menu(skill_main, tearoff=0)
        for skill in skill_main_values:
            skill_main_menu.add_command(
                label=skill, 
                command=lambda val=skill: self.skill_main.set(val),
                activebackground="#CDAF95"
            )
        skill_main["menu"] = skill_main_menu
        skill_main.pack(padx=10,pady=10, side=tk.LEFT)

        # 主技能加成
        self.skill_main_num= ttk.Entry(skill_main_box,bootstyle=WARNING,width=5)
        self.skill_main_num.pack(side="left",pady=10)

        # 等級
        tk.Label(skill_main_box, text="主技能等級：").pack(side="left",pady=10)
        self.skill_main_level = ttk.Entry(skill_main_box, style="WARNING", width=5)
        self.skill_main_level.pack(side="left",pady=10)

        # 能力提升
        tk.Label(skill_main_box, text="能力詳情").pack(side="left",padx=(100,10),pady=10)
        self.power_up = tk.StringVar()
        self.power_up.set("能力提升")
        power_up = ttk.Menubutton(skill_main_box,bootstyle=(OUTLINE,WARNING))
        power_up["textvariable"] = self.power_up
        power_up_values = ("無",'幫忙速度','活力回復量','EXP獲得量','食材發現率','主技能發動機率')
        power_up_menu = tk.Menu(power_up, tearoff=0)
        for ingredient in power_up_values:
            power_up_menu.add_command(
                label=ingredient, 
                command=lambda val=ingredient:self.power_up.set(val),
                activebackground="#CDAF95"
            )
        power_up["menu"] = power_up_menu
        power_up.pack(padx=10,pady=10, side=tk.LEFT)

        # 能力下降
        self.power_down = tk.StringVar()
        self.power_down.set("能力下降")
        power_down = ttk.Menubutton(skill_main_box,bootstyle=(OUTLINE,WARNING))
        power_down["textvariable"] = self.power_down
        power_down_values = ("無",'幫忙速度','活力回復量','EXP獲得量','食材發現率','主技能發動機率')
        power_down_menu = tk.Menu(power_down, tearoff=0)
        for ingredient in power_down_values:
            power_down_menu.add_command(
                label=ingredient, 
                command=lambda val=ingredient:self.power_down.set(val),
                activebackground="#CDAF95"
            )
        power_down["menu"] = power_down_menu
        power_down.pack(padx=10,pady=10, side=tk.LEFT) 

        # 副技能---------------------------------------
        skill_second_box = ttk.LabelFrame(self, text="副技能", style="WARNING")
        skill_second_box.pack(fill="x", padx=(10, 10), pady=10)

        # 副技能1
        self.skill_second_1 = tk.StringVar()
        self.skill_second_1.set("副技能1")
        skill_second_1 = ttk.Menubutton(skill_second_box,bootstyle=WARNING)
        skill_second_1["textvariable"] = self.skill_second_1
        skill_second_1_values = ('樹果數量','幫手獎勵','幫忙速度','睡眠EXP獎勵','研究EXP獎勵',
                                 '夢之碎片獎勵','活力恢復獎勵','食材機率提升','持有上限提升','技能機率提升','技能等級提升')
        skill_second_1_menu = tk.Menu(skill_second_1, tearoff=0)
        for skill in skill_second_1_values:
            skill_second_1_menu.add_command(
                label=skill, 
                command=lambda val=skill: self.skill_second_1.set(val),
                activebackground="#CDAF95"
            )
        skill_second_1["menu"] = skill_second_1_menu
        skill_second_1.pack(padx=10,pady=10, side=tk.LEFT)
        self.skill_second_num_1= ttk.Entry(skill_second_box,bootstyle=WARNING,width=5)
        self.skill_second_num_1.pack(side="left",pady=10)

        # 副技能2
        self.skill_second_2 = tk.StringVar()
        self.skill_second_2.set("副技能2")
        skill_second_2 = ttk.Menubutton(skill_second_box,bootstyle=WARNING)
        skill_second_2["textvariable"] = self.skill_second_2
        skill_second_2_values = ('樹果數量','幫手獎勵','幫忙速度','睡眠EXP獎勵','研究EXP獎勵',
                                 '夢之碎片獎勵','活力恢復獎勵','食材機率提升','持有上限提升','技能機率提升','技能等級提升')
        skill_second_2_menu = tk.Menu(skill_second_2, tearoff=0)
        for skill in skill_second_2_values:
            skill_second_2_menu.add_command(
                label=skill, 
                command=lambda val=skill: self.skill_second_2.set(val),
                activebackground="#CDAF95"
            )
        skill_second_2["menu"] = skill_second_2_menu
        skill_second_2.pack(padx=10,pady=10, side=tk.LEFT)
        self.skill_second_num_2= ttk.Entry(skill_second_box,bootstyle=WARNING,width=5)
        self.skill_second_num_2.pack(side="left",pady=10)

        # 副技能3
        self.skill_second_3 = tk.StringVar()
        self.skill_second_3.set("副技能3")
        skill_second_3 = ttk.Menubutton(skill_second_box,bootstyle=WARNING)
        skill_second_3["textvariable"] = self.skill_second_3
        skill_second_3_values = ('樹果數量','幫手獎勵','幫忙速度','睡眠EXP獎勵','研究EXP獎勵',
                                 '夢之碎片獎勵','活力恢復獎勵','食材機率提升','持有上限提升','技能機率提升','技能等級提升')
        skill_second_3_menu = tk.Menu(skill_second_3, tearoff=0)
        for skill in skill_second_3_values:
            skill_second_3_menu.add_command(
                label=skill, 
                command=lambda val=skill: self.skill_second_3.set(val),
                activebackground="#CDAF95"
            )
        skill_second_3["menu"] = skill_second_3_menu
        skill_second_3.pack(padx=10,pady=10, side=tk.LEFT)
        self.skill_second_num_3= ttk.Entry(skill_second_box,bootstyle=WARNING,width=5)
        self.skill_second_num_3.pack(side="left",pady=10)

        # 副技能4
        self.skill_second_4 = tk.StringVar()
        self.skill_second_4.set("副技能4")
        skill_second_4 = ttk.Menubutton(skill_second_box,bootstyle=WARNING)
        skill_second_4["textvariable"] = self.skill_second_4
        skill_second_4_values = ('樹果數量','幫手獎勵','幫忙速度','睡眠EXP獎勵','研究EXP獎勵',
                                 '夢之碎片獎勵','活力恢復獎勵','食材機率提升','持有上限提升','技能機率提升','技能等級提升')
        skill_second_4_menu = tk.Menu(skill_second_4, tearoff=0)
        for skill in skill_second_4_values:
            skill_second_4_menu.add_command(
                label=skill, 
                command=lambda val=skill: self.skill_second_4.set(val),
                activebackground="#CDAF95"
            )
        skill_second_4["menu"] = skill_second_4_menu
        skill_second_4.pack(padx=10,pady=10, side=tk.LEFT)
        self.skill_second_num_4= ttk.Entry(skill_second_box,bootstyle=WARNING,width=5)
        self.skill_second_num_4.pack(side="left",pady=10)

        # 副技能5
        self.skill_second_5 = tk.StringVar()
        self.skill_second_5.set("副技能5")
        skill_second_5 = ttk.Menubutton(skill_second_box,bootstyle=WARNING)
        skill_second_5["textvariable"] = self.skill_second_5
        skill_second_5_values = ('樹果數量','幫手獎勵','幫忙速度','睡眠EXP獎勵','研究EXP獎勵',
                                 '夢之碎片獎勵','活力恢復獎勵','食材機率提升','持有上限提升','技能機率提升','技能等級提升')
        skill_second_5_menu = tk.Menu(skill_second_5, tearoff=0)
        for skill in skill_second_5_values:
            skill_second_5_menu.add_command(
                label=skill, 
                command=lambda val=skill: self.skill_second_5.set(val),
                activebackground="#CDAF95"
            )
        skill_second_5["menu"] = skill_second_5_menu
        skill_second_5.pack(padx=10,pady=10, side=tk.LEFT)
        self.skill_second_num_5= ttk.Entry(skill_second_box,bootstyle=WARNING,width=5)
        self.skill_second_num_5.pack(side="left",pady=10)
    
        # 儲存按鈕---------------------------------------
        save_button = ttk.Button(self, text="儲存", command=self.save_to_database,bootstyle=WARNING)
        save_button.pack(pady=10)    

    # 創造 & 寫入資料庫
    def save_to_database(self,event=None):

        conn = sqlite3.connect("pokemon_database.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "img_num" INTEGER,
                "name" TEXT,
                "sp" INTEGER,
                "expertise" TEXT,
                "level" INTEGER,
                "help_fruit" TEXT,
                "help_fruit_num" INTEGER,
                "help_ingredient_1" TEXT,
                "help_ingredient_num_1" INTEGER,
                "help_ingredient_2" TEXT,
                "help_ingredient_num_2" INTEGER,
                "help_ingredient_3" TEXT,
                "help_ingredient_num_3" INTEGER,
                "help_time" TEXT,
                "help_max" INTEGER,
                "skill_main" TEXT,
                "skill_main_num" REAL,
                "skill_main_level" INTEGER,
                "skill_second_1" TEXT,
                "skill_second_num_1" REAL,
                "skill_second_2" TEXT,
                "skill_second_num_2" REAL,
                "skill_second_3" TEXT,
                "skill_second_num_3" REAL,
                "skill_second_4" TEXT,
                "skill_second_num_4" REAL,
                "skill_second_5" TEXT,
                "skill_second_num_5" REAL,
                "power_up" TEXT,
                "power_down" TEXT
            )
        ''')

        # 把輸入資料引入
        img_num=self.img_num.get()
        name = self.name.get()
        sp=self.sp.get()
        expertise = self.expertise.get()
        level=self.level.get()
        help_fruit=self.help_fruit.get()
        help_fruit_num=self.help_fruit_num_1.get()
        help_ingredient_1=self.help_ingredient_1.get()
        help_ingredient_num_1=self.help_ingredient_num_1.get()
        help_ingredient_2=self.help_ingredient_2.get()
        help_ingredient_num_2=self.help_ingredient_num_2.get()
        help_ingredient_3=self.help_ingredient_3.get()
        help_ingredient_num_3=self.help_ingredient_num_3.get()
        help_time=self.help_time.get()
        help_max=self.help_max.get()
        skill_main=self.skill_main.get()
        skill_main_num=self.skill_main_num.get()
        skill_main_level=self.skill_main_level.get()
        skill_second_1=self.skill_second_1.get()
        skill_second_num_1=self.skill_second_num_1.get()
        skill_second_2=self.skill_second_2.get()
        skill_second_num_2=self.skill_second_num_2.get()
        skill_second_3=self.skill_second_3.get()
        skill_second_num_3=self.skill_second_num_3.get()
        skill_second_4=self.skill_second_4.get()
        skill_second_num_4=self.skill_second_num_4.get()
        skill_second_5=self.skill_second_5.get()
        skill_second_num_5=self.skill_second_num_5.get()
        power_up=self.power_up.get()
        power_down=self.power_down.get()

        # 存入sql
        cursor.execute('''
            INSERT INTO pokemon (
                "img_num",
                "name",
                "sp",
                "expertise",
                "level",
                "help_fruit",
                "help_fruit_num",
                "help_ingredient_1",
                "help_ingredient_num_1",
                "help_ingredient_2",
                "help_ingredient_num_2",
                "help_ingredient_3",
                "help_ingredient_num_3",
                "help_time",
                "help_max",
                "skill_main",
                "skill_main_num",
                "skill_main_level",
                "skill_second_1",
                "skill_second_num_1",
                "skill_second_2",
                "skill_second_num_2",
                "skill_second_3",
                "skill_second_num_3",
                "skill_second_4",
                "skill_second_num_4",
                "skill_second_5",
                "skill_second_num_5",
                "power_up",
                "power_down"
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            img_num,
            name,
            sp,
            expertise,
            level,
            help_fruit,
            help_fruit_num,
            help_ingredient_1,
            help_ingredient_num_1,
            help_ingredient_2,
            help_ingredient_num_2,
            help_ingredient_3,
            help_ingredient_num_3,
            help_time,
            help_max,
            skill_main,
            skill_main_num,
            skill_main_level,
            skill_second_1,
            skill_second_num_1,
            skill_second_2,
            skill_second_num_2,
            skill_second_3,
            skill_second_num_3,
            skill_second_4,
            skill_second_num_4,
            skill_second_5,
            skill_second_num_5,
            power_up,
            power_down
        ))

        conn.commit()
        conn.close()
        self.destroy()
    
    def show_fruit_image(self, event):
        img_path = '对应的图像路径'
        self.show_image(img_path)

    # 顯示樹果圖片
    def show_image(self, img_num):
        try:
            img = Image.open('display_data/fruit.jpg')
            width, height = img.size
            new_width = int(width * 0.4)
            new_height = int(height * 0.4)
            img = img.resize((new_width, new_height))
            tk_img = ImageTk.PhotoImage(img)

            x_pos = self.winfo_x() + self.winfo_width() + 10
            y_pos = self.winfo_y()-50

            self.jpg = tk.Toplevel()
            self.jpg.title("樹果類型")
            self.jpg.geometry(f'+{x_pos}+{y_pos}')

            label = tk.Label(self.jpg, image=tk_img)
            label.image = tk_img
            label.pack()
        except FileNotFoundError:
            print("找不到图像")

# 主介面的Tree View
class PokemonTreeView(ttk.Treeview):
    def __init__(self,parent,**kwargs):
        super().__init__(parent,**kwargs)
        self.parent=parent
        self.conn=sqlite3.connect("pokemon_database.db")
        
        # 欄位名稱
        self.heading('id',text="id")
        self.heading('name',text='名稱')
        self.heading('help_fruit',text="樹果類型")
        self.heading('help_ingredient_1',text="食材類型")
        # 欄寬
        self.column('id',width=25)
        self.column('name',width=60)
        self.column('help_fruit',width=70)
        self.column('help_ingredient_1',width=80)

        self.load_data()
    
    # 引入datbase資料
    def load_data(self):
        cursor=self.conn.cursor()
        cursor.execute('''
                        SELECT id,name,help_fruit,help_ingredient_1
                       FROM pokemon
                       ''')
        rows=cursor.fetchall()

        for item in self.get_children():
            self.delete(item)

        for row in rows:
            self.insert('',"end",values=row)
    
    # 搜尋後的tree view介面
    def display_data(self, data):
        if not data.empty:

            self.delete(*self.get_children())
            # 欄位名稱
            self.heading('id',text="id")
            self.heading('name',text='名稱')
            self.heading('help_fruit',text="樹果類型")
            self.heading('help_ingredient_1',text="食材類型")
            # 欄寬
            self.column('id',width=25)
            self.column('name',width=60)
            self.column('help_fruit',width=70)
            self.column('help_ingredient_1',width=80)
            
            column=['id','name','help_fruit','help_ingredient_1']

            for _,row in data.iterrows():
                    values = [row[col] for col in column]
                    self.insert("", "end", values=values)

if __name__ == "__main__":
    window=Window()
    window.title("Pokemon Sleep SQL")
    window.resizable(width=False,height=False)
    window.mainloop()
