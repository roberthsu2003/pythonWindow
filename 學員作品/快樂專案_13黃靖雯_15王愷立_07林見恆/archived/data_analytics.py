73% of storage used … If you run out, you can't create, edit, and upload files. Get 100 GB of storage for NT$65.00 NT$0 for 1 month.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 读取 CSV 文件
file_path = '/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/World Happiness Report_new.csv'
happiness_report = pd.read_csv(file_path)

# 填充缺失值
happiness_report.fillna(happiness_report.mean(numeric_only=True), inplace=True)

# 确认存在的列名，并定义特征和目标变量
available_columns = happiness_report.columns
print(f"Available columns: {available_columns}")

# 根据数据框中的实际列名定义特征和目标变量
features = [col for col in ['Log GDP Per Capita', 'Social Support', 'Healthy Life Expectancy', 'Freedom to Make Life Choices', 'Generosity', 'Perceptions of Corruption'] if col in available_columns]
target = 'Life Ladder'

# 标准化数据
scaler = StandardScaler()
happiness_report[features] = scaler.fit_transform(happiness_report[features])

# 分割数据集
X = happiness_report[features]
y = happiness_report[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 建立线性回归模型
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# 建立随机森林模型
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 预测并计算均方误差和R²分数
lr_predictions = lr_model.predict(X_test)
rf_predictions = rf_model.predict(X_test)

lr_mse = mean_squared_error(y_test, lr_predictions)
rf_mse = mean_squared_error(y_test, rf_predictions)

lr_r2 = r2_score(y_test, lr_predictions)
rf_r2 = r2_score(y_test, rf_predictions)

print(f"Linear Regression - MSE: {lr_mse}, R²: {lr_r2}")
print(f"Random Forest - MSE: {rf_mse}, R²: {rf_r2}")

# 提取特征重要性
lr_feature_importance = pd.DataFrame({'Feature': features, 'Coefficient': lr_model.coef_})
rf_feature_importance = pd.DataFrame({'Feature': features, 'Importance': rf_model.feature_importances_})

# 生成相关性热力图
numeric_cols = happiness_report.select_dtypes(include=[float, int]).columns
plt.figure(figsize=(12, 10))
corr = happiness_report[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Heatmap")
plt.show()

# 生成线性回归特征重要性图
plt.figure(figsize=(10, 8))
sns.barplot(x='Feature', y='Coefficient', data=lr_feature_importance)
plt.title("Linear Regression Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 生成随机森林特征重要性图
plt.figure(figsize=(10, 8))
sns.barplot(x='Feature', y='Importance', data=rf_feature_importance)
plt.title("Random Forest Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()