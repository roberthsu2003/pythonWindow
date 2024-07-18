### 主程式 FINAL>window.py

![封面圖](螢幕擷取畫面%202024-07-18%20102238.png)

### 專案連結:有詳細說明
https://github.com/LanvisWei/MLproject_Solar_Irradiance

### 專案目的
評估太陽能系統建置可能及實用性

### 功能


> 等效日射小時（Equivalent Sun Hours, ESH）

> 來源：
> * Solarmazd​ ([SOALRMAZD](https://solarmazd.com/peak-sun-hours-psh-what-does-it-mean-and-how-to-estimate-it/))​
> * RenewableWise​ ([Renewablewise](https://www.renewablewise.com/peak-sun-hours-calculator/))​
> * Palmetto​ ([Palmetto](https://palmetto.com/solar/what-are-peak-sun-hours))​
> * Dot Watts​ ([Dot Watts®](https://palmetto.com/solar/what-are-peak-sun-hours))

等效日射小時表示一天內太陽能輻射量轉化為在1千瓦每平方公尺（1kW/m²）條件下工作的總時間。這個指標有助於評估太陽能系統在特定地區的性能。等效日射小時的計算公式如下：

> ESH = DailySolarIrradiation (kWh/m²/day) / (1kW/m²)**
> * 如果某地一天接收到 6 kWh/m² 的太陽能量，則該地的 ESH 為 6 小時，意味著該地接收到相當於 6 小時的 1000 W/m² 的陽光。

> * Daily Energy Production=Power Rating of Panel×ESH

    - 每日能量產出=太陽能板功率×ESH

> * example : If you have a 200-watt solar panel and the ESH in your location is 5 hours. Daily Energy Production=200 W×5 hours=1,000 Wh or 1 kWh.

    - 如果你有一塊 200 瓦的太陽能板，而你所在位置的 ESH 為 5 小時，每日能量產出=200 W×5 小時=1000 Wh 或 1 kWh

### 資料來源

- 交通部中央氣象署 首頁>生活>農業>農業觀測>全部觀測網月資料
    * [日射量資料](https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html)
    * 使用selenium獲取資料並輸出.csv

### 重要計算式

- MJ/m² 轉換為kW/m² 的公式：1 MJ/m² = 0.2778 kW/m²

- P=Sxη×ESH/E
    * S 是系統容量(KW)
    * E 是每日能量需求（kWh/day）
    * η 是系統效率

### 結論

![01](./螢幕擷取畫面%202024-07-18%20102631.png)
![02](./螢幕擷取畫面%202024-07-18%20102655.png)
![03](./螢幕擷取畫面%202024-07-18%20102714.png)
![04](./螢幕擷取畫面%202024-07-18%20002159.png)
![05](./螢幕擷取畫面%202024-07-18%20002313.png)
![06](./螢幕擷取畫面%202024-07-18%20002343.png)

1. 讓你相信未來會越來越熱
2. 讓你知道在台灣裝不裝太陽能供電系統其實跟太陽沒關係
3. 讓你知道台灣的家用太陽能系統其實跟你有多少地有關係
4. 然後你會知道有多少地跟你有多少錢有關係
5. 讓你知道綠能很美好，但建構起來完全不符合效率也不符合CP值，太陽能中，太陽能板的成本其實並不是其中最大的比重。

### [影片](https://youtu.be/Ep1lNgUoSw8)