# 寵物登記數預測工具  
## 一、專案名稱：寵物登記數預測工具 
預設畫面->全臺往年寵物登記趨勢
![專案/README_img/截圖 2024-11-25 上午8.53.49.png](https://github.com/joy273609/python_windows/blob/main/%E5%B0%88%E6%A1%88/README_img/%E6%88%AA%E5%9C%96%202024-11-25%20%E4%B8%8A%E5%8D%888.53.49.png?raw=true)
## 二、專案組員：周禹彤、呂安杰  
## 三、專案網址  
[寵物登記數預測工具 Git Hub 連結](https://github.com/roberthsu2003/__2024_09_04_tvdi__/tree/main/%E5%AD%B8%E5%93%A1%E4%BD%9C%E6%A5%AD/%E5%AF%B5%E7%89%A9%E7%99%BB%E8%A8%98%E6%95%B8%E9%A0%90%E6%B8%AC%E5%B7%A5%E5%85%B7_%E5%91%A8%E7%A6%B9%E5%BD%A4%E3%80%81%E5%91%82%E5%AE%89%E6%9D%B0)

## 四、專案目的  
分析過往寵物登記數量的增長或下降趨勢、去預測未來登記數量的變化，以了解寵物登記率的變動。

## 五、資料來源  
[寵物登記管理資訊網](https://www.pet.gov.tw/Web/O302.aspx)  
使用農業部公開資訊網站  

## 六、程式設計  
### 資料蒐集  
1. **selenium**   
* 利用 *selenium* 進行網頁自動化操作。
* 利用 *webdriver* 控制瀏覽器的核心。
* 利用 *Service* 管理瀏覽器驅動程式（例如 ChromeDriver）。
* 利用 *By* 定位網頁元素的方法（如使用 class name 或 id）。
* 利用 *WebDriverWait* 和 *EC* 設置動態等待條件。

2. **BeautifulSoup**  
* 利用 *BeautifulSoup* 進行html網頁架構分析，便於提取特定部分內容。

3. **pandas**  
* 利用 *pandas* 處理表格數據，將列表資料轉換成表格DataFrame，最後導出 CSV 文件。

### GUI介面設計
允許使用者選擇地區，選擇地區後，模型會自動填入該地區2009至2023的登記數量、絕育數量、除戶數量和絕育率之等數據。  
  
地區登記及絕育趨勢圖：顯示過去幾年該地區的寵物登記數趨勢圖，幫助使用者了解該地區的長期變化。  

1. **tkinter** 和 **ttk**  
 * 利用 *tkinter* 和 *ttk* 建構主視窗界面
 * 利用 *tkintermapview*  顯示地圖和互動功能的第三方庫
 * 利用 *ttk.Treeview* 顯示年度統計數據

2. **map_renderer**  
 * 利用 *TaiwanMapRenderer* 顯示台灣地圖
 * 利用 *TaiwanMapRenderer* 為每個縣市設定座標、建立地圖標記
 * 利用 *TaiwanMapRenderer* 設定使用者點擊觸發事件
 * 利用 *TaiwanMapRenderer* 點擊時的動態改變標記狀態及地圖視角
 * 利用 *TaiwanMapRenderer* 進行資源管理，在跳轉下一個觸發事件時，會清除先前所有紀錄

3. **matplotlib**    
 * 利用 *matplotlib* 繪製圖表
 * 利用 *plt.rcParams* 設定中文介面
 * 利用 *FigureCanvasTkAgg* 將 Matplotlib 圖表嵌入到 Tkinter 的 GUI 應用程式中

4. **numpy**  
利用 *np.divide* 計算絕育數與登記數的比率

5. **src.ui.analysis_view**  
 * 利用 *src.ui.analysis_view* 匯入分析視圖模組
 * 利用 *AnalysisView* 顯示數據分析內容

6. **src.data.data_source**   
利用 *src.data.data_source* 匯入資料管理器，處理寵物登記與絕育相關的數據。


## 七、完成示意圖 
**臺北市**往年的登記數據
![觀看**臺北市**往年的登記數據](https://github.com/joy273609/python_windows/blob/main/%E5%B0%88%E6%A1%88/README_img/%E6%88%AA%E5%9C%96%202024-11-25%20%E4%B8%8A%E5%8D%888.54.48.png?raw=true)  

**高雄市**往年的登記數據
![觀看**高雄市**往年的登記數據](https://github.com/joy273609/python_windows/blob/main/%E5%B0%88%E6%A1%88/README_img/%E6%88%AA%E5%9C%96%202024-11-25%20%E4%B8%8A%E5%8D%888.55.07.png?raw=true)  

**花蓮市**往年的登記數據
![觀看**花蓮市**往年的登記數據](https://github.com/joy273609/python_windows/blob/main/%E5%B0%88%E6%A1%88/README_img/%E6%88%AA%E5%9C%96%202024-11-25%20%E4%B8%8B%E5%8D%889.07.10.png?raw=true)  


## 八、Vedio Demo
[寵物登記數預測工具 on YouTube](https://youtu.be/6lvEv9bwV5U)
