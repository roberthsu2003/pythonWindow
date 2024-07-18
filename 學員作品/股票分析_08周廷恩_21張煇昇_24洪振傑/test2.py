import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.decomposition import PCA


data =pd.read_csv('202006202312.csv')

def KNeighbors():
    tdf= pd.DataFrame()

    tdf['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 'Buy', 'Sell')
    
    # 根据需求处理第一个时间点的情况，这里假设默认为 'Sell'
    tdf.loc[0, 'Target'] = 'Sell'

    x = data.iloc[:, 1:-1].values  # 假設需要排除第一列（日期）和最後兩列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作為目標變量

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4,random_state=39830)

    # 使用 KNeighborsClassifier 進行訓練和評分
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(x_train, y_train)
    score = knn.score(x_test, y_test)
    print(f"knn 最佳準確率: {score}")

def GridSearch():
    tdf= pd.DataFrame()

    tdf['Target'] = np.where(data['Close'].diff() > 0, 'Buy', 'Sell')

    x = data.iloc[:, 1:-1].values  # 假設需要排除第一列（日期）和最後兩列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作為目標變量

    x_train , x_test , y_train , y_test = train_test_split(
    x,y, test_size=0.4,random_state=39830)
    param = {'n_neighbors':[3,5,8,10],
            'weights':['uniform','distance']}
    knn = KNeighborsClassifier()
    gc = GridSearchCV(knn, param_grid=param, cv=5)
    gc.fit(x_train,y_train)
    print('網格 最佳準確率：')
    print(gc.best_score_)
    print('網格 最佳參數組合：')
    print(gc.best_estimator_)

def Decision_tree(random_state):
    
    tdf = pd.DataFrame()
    tdf['Target'] = data['Close']

    f = ['Open', 'High', 'Low', 'Adj Close', 'EMA12']
    x = data[f].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=random_state)

    dec = DecisionTreeRegressor(random_state=random_state)
    dec.fit(x_train, y_train)

    # 在测试集上评估模型
    y_pred = dec.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Decision_tree 均方誤差: {mse}")
    print(f"Decision_tree R^2 分數: {r2}")

    return mse, r2

def Decision_tree_graph():
    features = ['High','Low','Open','Adj Close','EMA12']
    X = data[features]

    tdf= pd.DataFrame()
    tdf['Target'] =data['Close']
    y = tdf['Target'].values  # 使用 'Target' 作為目標變量
    
    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(X, y)
    tree.plot_tree(classifier)
    plt.show()

def Linear_regression():
    tdf = pd.DataFrame()
    tdf['Target'] = data['Close']

    f =['Open','High','Low','Adj Close','EMA12']
    x = data[f].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x = data.iloc[:, 1:-1].values  # 假設需要排除第一列（日期）和最後兩列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作為目標變量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4,random_state=39830)
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    print('權重值：{}'.format(lr.coef_))
    print('偏置值：{}'.format(lr.intercept_))

    y_predict = std_y.inverse_transform(lr.predict(x_test))
    y_real = std_y.inverse_transform(y_test)
    for i in range(50):
        print('預測值：{}，真實值：{}'.format(y_predict[i], y_real[i]))

    merror = mean_squared_error(y_real, y_predict)
    print('平均方差：{}'.format(merror))

def DR_Linear_regression():
    tdf= pd.DataFrame()

    tdf['Target'] = data['Close']

    f =['Open','High','Low','Adj Close','EMA12']
    x = data[f].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4,random_state=39830)
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))
    sgd = SGDRegressor()
    sgd.fit(x_train, y_train)
    print('權重值：{}'.format(sgd.coef_))
    print('偏置值：{}'.format(sgd.intercept_))
    y_predict = std_y.inverse_transform(sgd.predict(x_test).reshape(-1, 1))
    y_real = std_y.inverse_transform(y_test)
    for i in range(20):
        print('DR_預測值：{}，DR_真實值：{}'.format(y_predict[i], y_real[i]))
    merror = mean_squared_error(y_real, y_predict)
    print('DR_平均方差：{}'.format(merror))

def Logisticregression():
    tdf= pd.DataFrame()

    tdf['Target'] = np.where(data['Close'].diff() > 0, 'Buy', 'Sell')

    x = data.iloc[:, 1:-1].values  # 假設需要排除第一列（日期）和最後兩列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作為目標變量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4,random_state=39830)
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    estimator = LogisticRegression()
    estimator.fit(x_train, y_train)
    score = estimator.score(x_test, y_test)
    print("Logistic 準確率：{}".format(score))

def classificationreport():
    tdf = pd.DataFrame()
    tdf['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 'Buy', 'Sell')
    
    # 根据需求处理第一个时间点的情况，这里假设默认为 'Sell'
    tdf.loc[0, 'Target'] = 'Sell'

    x = data.iloc[:, 1:-1].values  # 假設需要排除第一列（日期）和最後兩列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作為目標變量

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=39830)

    estimator = LogisticRegression()
    estimator.fit(x_train, y_train)
    y_pre = estimator.predict(x_test)

    le = LabelEncoder()
    y_test = le.fit_transform(y_test)
    y_pre = le.fit_transform(y_pre)

    ret = classification_report(y_test, y_pre, labels=(0, 1),
                                target_names=("買", "賣"), zero_division=0)
    print(ret)

def svc():
    tdf = pd.DataFrame()
    tdf['Target'] = np.where(data['Close'].diff() > 0, 'Buy', 'Sell')

    f =['Open','High','Low','Adj Close','EMA12']
    x = data[f].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4,random_state=39830)
    clf = SVC(kernel='linear', gamma='scale', C=1, degree=3)
    clf.fit(x_train,y_train)
    score = clf.score(x_test, y_test)
    print("準確率：{}".format(score))

def svcandpca():
    tdf = pd.DataFrame()
    tdf['Target'] = data['Close']

    f =['Open','High','Low','Adj Close','EMA12']
    x = data[f].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4,random_state=39830) #random_state=1 使資料分割固定
    pca =PCA(svd_solver='randomized', n_components=5, whiten=True)
    pca.fit(x, y)
    x_train_pca = pca.transform(x_train)
    x_test_pca = pca.transform(x_test)
    clf = SVC(kernel='rbf', C=100, gamma='auto')
    clf = clf.fit(x_train_pca, y_train)
    predict = clf.predict(x_test_pca)
    score = clf.score(x_test_pca, y_test)
    print("準確率：{}".format(score))
    for i in range(20):
        print('預測值：{}，真實值：{}'.format(predict[i],y_test[i]))

def svm():
    tdf = pd.DataFrame()
    tdf['Target'] = data['Close']

    f =['Open','High','Low','Adj Close','EMA12']
    x = data[f].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4,random_state=39830)
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))
    clf = SVR(kernel='rbf', C=1, gamma='auto')
    clf.fit(x_train, y_train)
    y_predict = clf.predict(x_test)
    y_predict = std_y.inverse_transform(y_predict.reshape(-1, 1))
    y_real = std_y.inverse_transform(y_test)
    for i in range(min(20, len(y_predict))):  # 打印前20个元素或者数组的长度，取两者中较小的值
        print('預測值：{}，真實值：{}'.format(y_predict[i][0], y_real[i][0]))
    merror = mean_squared_error(y_real, y_predict)
    print('平均方差：{}'.format(merror))
    
# KNeighbors()
# GridSearch()
# Decision_tree(39830)
# Linear_regression()
# DR_Linear_regression()
# Logisticregression()
# classificationreport()
svc()
# svcandpca()
# svm()

# best_score = -1
# best_random_state = None

# for random_state in range(100000):  # 尝试多个随机种子
#     score = Decision_tree(random_state)
#     if score > best_score:
#         best_score = score
#         best_random_state = random_state

# print(f'在 random_state={best_random_state} 下的最佳准确率为: {best_score:.4f}')

# Decision_tree_graph()