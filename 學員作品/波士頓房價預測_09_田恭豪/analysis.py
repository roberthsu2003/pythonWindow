import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# 讀取數據集
data = pd.read_csv('train_dataset.csv')

# 假設 'selectedFeatures' 包含你要選取的欄位名稱：
selectedFeatures = ['LSTAT', 'RM']  # 更換成你實際的欄位名稱

# 提取特徵和目標變數
X = data[selectedFeatures]
y = data['PRICE']

# 初始化最高準確率及其對應的模型名稱
max_knn_accuracy = -1
max_gs_accuracy = -1
max_dec_accuracy = -1

# 迭代運行五次並找出最高準確率的一次
for i in range(5):
    # 分割數據集為訓練集和測試集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)

    # 標準化數據
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 使用K近鄰演算法
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    knn_score = knn.score(X_test_scaled, y_test)
    if knn_score > max_knn_accuracy:
        max_knn_accuracy = knn_score

    # 設定KNN回歸模型和GridSearchCV的參數網格
    param_grid = {
        'n_neighbors': [3, 5, 8, 10],
        'weights': ['uniform', 'distance']
    }

    knn_gs = KNeighborsRegressor()
    grid_search = GridSearchCV(knn_gs, param_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X_train_scaled, y_train)
    gs_score = grid_search.best_estimator_.score(X_test_scaled, y_test)
    if gs_score > max_gs_accuracy:
        max_gs_accuracy = gs_score

    # 初始化決策樹回歸模型
    dec_tree = DecisionTreeRegressor(random_state=42)
    dec_tree.fit(X_train, y_train)
    dec_score = dec_tree.score(X_test, y_test)
    if dec_score > max_dec_accuracy:
        max_dec_accuracy = dec_score

# 輸出最高準確率
print(f"K近鄰模組_準確率：{max_knn_accuracy}")
print(f"GridSearchCV網格搜索模組_準確率：{max_gs_accuracy}")
print(f"決策樹分析_準確率：{max_dec_accuracy}")
