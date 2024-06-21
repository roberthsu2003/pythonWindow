# 實際案例

1. [1顯示表格資料使用CSV](./1顯示表格資料使用CSV/sample1_displayCSV_Grid.py)

![顯示表格資料使用CSV](./images/pic1.png)

---

1-1. [顯示表格資料使用網路爬蟲和Toplevel](./1-1爬蟲和使用Toplevel/main.py)

- 使用toplevel
  
- 使用2個自訂package

![顯示表格資料使用網路爬蟲和Toplevel](./images/pic1-1-1.png)
![顯示表格資料使用網路爬蟲和Toplevel](./images/pic1-1-2.png)


---


2. [顯示表格資料使用sqlite](./2顯示表格資料使用sqlite/sample2_displayTable_sqlite.py)

![顯示表格資料](./images/pic1.png)

---

3. [顯示表格資料使用網路爬蟲和自訂Dialog類別](./1-2爬蟲和使用自訂Dialog/main.py)

- 繼承Dialog類別
- 使用List類別和ScrollBar
- 使用2個自訂package

![顯示表格資料使用網路爬蟲和Toplevel](./images/pic1-2-1.png)
![顯示表格資料使用網路爬蟲和Toplevel](./images/pic1-2-2.png)

---



4. [建立ListBox+ScrollBar和Convas+ScrollBar,顯示單筆資料](./4listBox_ScrollBar_Convas/sample4_displayOneRow_listbox.py)
> 注意:必需先學習Convas的使用方法

![](./images/pic2.png)

---

5. [使用Treeview建立表格資料和TopLevel的操控](./5treeView_topLevel/sample5_displayTable_TreeView_topLevel.py)

![](./images/pic4.png)

![](./images/pic5.png)

---

6. [使用Treeview建立表格資料和自訂Dialog類別](./6treeview和自訂Dialog類別/sample6_displayTable_TreeView_Dialog.py)

![](./images/pic4.png)

![](./images/pic6.png)

---

7-1. [顯示政府開放平台空氣品質指標簡易版](./7顯示政府開放平台空氣品質指標簡易版/sample8_顯示目前空氣品質.py)

![](./images/pic7.png)

---

7-2. [顯示政府開放平台空氣品質指標_儲存下載json檔案正式版](./7-2顯示政府開放平台空氣品質指標正式版/main.py)

![](./images/pic8.png)

---

7-3. [顯示政府開放平台空氣品質_分欄位的版本](./空氣品質指標aqi_csv_多欄位版/main.py)

![](./空氣品質指標aqi_csv_多欄位版/images/pic1.png)

---

7-4.[顯示政府開放平台空氣品質_canvas_scrollbar](./空氣品質指標aqi_csv_canvas_scrollbar/main.py)

![](./空氣品質指標aqi_csv_canvas_scrollbar/images/pic1.png)

---


9.[台北市youbike及時資料](./台北市youbike/index.py)

![](./images/pic9.png)

---

9-1. [台北市youbike及時資料簡易版(無計時)](./簡易版youbike/youbikeOfTaipei.py)

![](./簡易版youbike/images/pic1.png)

9-2 [台北市youbike可停_可借_及時更新資訊](./台北市youbike1/youbike.py)

 - 使用繼承LabelFrame,讓程式可讀性和維護更方便
 - 使用TreeView
 - 使用sqlite儲存資料,資料不會重覆,使用Replace
 - 每隔10秒更新一次資料

![](./台北市youbike1/images/pic1.png)
---


10. [股票及時查詢系統](./10-1台灣證券交易所及時股票查詢系統/main.py)

![](./images/pic10.png)

---

11.[台北市youbike2.0即時資訊_地圖](./11台北市youbike2.0_地圖/main.py)

![](./images/pic11.png)

---

12.[股票即時爬蟲,儲存為csv檔,並顯示](./12_13即時存csv檔,顯示線圖/index1.py)
 - data.py(負責爬蟲和儲存為csv檔,data.py要先執行才有資料存檔)
 - index1.py(負責即時顯示)

![](./images/pic12.png)

---

13 [顯示4檔股票近2年的歷史線圖](./12_13即時存csv檔,顯示線圖/index1.py)
- index.py

![](./images/pic13.png)

---

14 [全台4天天氣預測](./14全台4天天氣預測/index.py)
- index.py

![](./images/pic14.png)

---

15 [台北市youbike](./15台北市youbike/index.py)
- 使用sqlite
- 每3分鐘收集youbike資訊,資料為累加的資料
- 繼承Dialog
- 搜尋功能

![](./images/pic15.png)
![](./images/pic16.png)

---

16 [台北市youbike_postgreSQL](./16台北youbike_postgreSQL/index.py)
- 使用render_postgreSQL
- 使用psycopg2-binary module
- 使用pgAdmin4管理資料庫
- 每3分鐘收集youbike資訊,資料為累加的資料
- 繼承Dialog
- 搜尋功能

![](./images/pic15.png)

---

17 [BMI計算器](./17BMI計算器/index.py)

- grid_layout
- 繼承Dialog
- Dialog內,操控parent window內的widget

![](./images/pic17_1.png)
![](./images/pic17_2.png)
![](./images/pic17_3.png)

---

18 [youbike_圖表動態顯示](./18youbike_圖表動態顯示/index.py)
- pydantic
- ttkthemes
- FigureCanvasTkAgg(顯示圖表)
- 處理圖表太佔記憶體的問題
- 繼承Frame

![](./images/pic18.png)

---