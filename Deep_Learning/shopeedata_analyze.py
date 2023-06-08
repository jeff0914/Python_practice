from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from tensorflow.keras.callbacks import EarlyStopping

df_train = pd.read_csv('product_overview_20210401-20230409_final.csv')
print(df_train.describe())  #簡單的敘述統計
print(df_train.head())
corrmat = df_train.corr()  #相關係數可直接丟入sns.heatmap
k = 10 #顯現幾個特徵
cols = corrmat.nlargest(k, 'total_sales')['total_sales'].index#顯現和k個相近的關係變量矩陣的名稱
print(cols)
print(df_train[cols].values)

cm = np.corrcoef(df_train[cols].values.T)  #轉置後才符合np.corrcoef格式
sns.set(font_scale=1.25)#字體比例
hm = sns.heatmap(cm,                        # col val
                 cbar=True,                 # 顏色條    
                 annot=True, square=True,   #  劃出數值 正方形
                 fmt='.2f',                 # 小數點幾位
                 annot_kws={'size': 10},    # 數值參數可設置顏色加粗斜體等
                 yticklabels=cols.values,   
                 xticklabels=cols.values)  
plt.show()

dataset = np.loadtxt("product_overview_20210401-20230409_final.csv", 
                     delimiter=",",
                     skiprows=1, #跳過第一行
                     dtype="int",
                   )
data = dataset[:, 0:7]    # 資料集
label = dataset[:, 8]
mean = np.mean(label)    #  平均數
median = np.median(label)#  中位數
label_bin = np.array([1 if i>2217 else 0 for i in label]) #把label>2217部分變1否則變0


bins = np.arange(0, 14000, 1000) #直方圖寬
plt.hist(label,bins=bins)
plt.axvline(mean, color='r', linestyle='dashed', linewidth=2)
plt.axvline(median, color='g', linestyle='dashed', linewidth=2)

# 設定標題與軸標籤
plt.title('Sample Data with Mean and Median')
plt.xlabel('Value')
plt.ylabel('Frequency')

# 顯示圖形
plt.show()
print("mean : ", mean)   
print("median : ",median) 
print(type(data))
print(type(label_bin))
print("data維度:",data.shape)
print("label_bin維度:",label_bin.shape)

model = Sequential()
model.add(Dense(128, input_dim=7, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

print(model.summary()) 

# 編譯模型
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# 訓練模型   迭代100次、批處理大小為10,
early_callback = EarlyStopping(
                            monitor="loss",min_delta=0.001,
                            patience=10,verbose=1,mode="auto")
history = model.fit(data, label_bin, epochs=100, batch_size=10,
                    validation_split = 0.3,    # 劃分資料集的 30% 作為驗證集用
                    verbose = 2,callbacks=[early_callback])               # 印出為精簡模式
print("history: ",history.history) 

# 評估模型
loss, accuracy = model.evaluate(data, label_bin)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
# 數據預測
probabilities = model.predict(data)

x = [i for i in range(1,736)]
plt.scatter(x[0:100],label_bin[0:100],color = 'green',label="Original data")
# 繪製訓練集的預測資料
plt.scatter(x[0:100],predictions[0:100], color = 'red',label="Train data Predict",alpha = 0.2)
