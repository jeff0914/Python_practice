from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import numpy as np

dataset = np.loadtxt('./product_overview_selected_medine.csv', delimiter=",")
# data set 依據欄位數調整
data = dataset[:,0:9]
label = dataset[:,9]

print(data.shape)
print(label.shape)


from tensorflow.keras.layers import Dense 
model = Sequential()
model.add(Dense(12,input_dim = 9, activation = 'relu'))
model.add(Dense(8, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))
print(model.summary())

from sklearn.model_selection import train_test_split

train_data, test_data, train_label, test_label = train_test_split(data, label, test_size=0.4, random_state=42)

# 訓練集
print(train_data.shape)
print(train_label.shape)

# 測試集
print(test_data.shape)
print(test_label.shape)


model.compile(loss = 'binary_crossentropy', 
              optimizer='adam',
              metrics=['accuracy'])
history = model.fit(data,label,epochs=100,
                    batch_size=10, 
                    validation_split=0.4, 
                    verbose=2)
print(history.history)


loss,accuracy = model.evaluate(data,label)
print("\n loss:%.2f, accuracy:%.2f" %(loss,accuracy))
probabilities = model.predict(data)
prediction = [float(np.round(x))for x in probabilities]
accuracy = np.mean(prediction == label)
print("prediction accuracy : % .2f" %accuracy)