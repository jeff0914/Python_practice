import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
# 讀取 CSV 檔案
file_path = './product_overview_selected_medinev2.csv'
df = pd.read_csv(file_path)

# df['date_time'] = pd.to_datetime(df['date_time'])

# # 將 datetime 對象轉換為數值表示（例如，通過計算自某個基準日期以來的天數）
# df['date_time_numeric_days'] = (df['date_time'] - pd.Timestamp("1970-01-01")) // pd.Timedelta("1D")
# df = df.drop(columns=['date_time'])

X = df.drop(columns=['sale_grades'])
y = df['sale_grades']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
# 創建隨機森林模型
rf = RandomForestRegressor()
# 訓練模型
rf.fit(X_train, y_train)

# 預測測試集
y_pred = rf.predict(X_test)

# 計算 R2 分數
r2 = r2_score(y_test, y_pred)
print(f"R2 Score: {r2}")