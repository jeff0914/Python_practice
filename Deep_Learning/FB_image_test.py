import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Flatten, Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from sklearn.utils import class_weight
from imblearn.over_sampling import RandomOverSampler

import json

# path = '/content/drive/MyDrive/Colab Notebooks' # on colab
path = '.'  # on local side

with open(f'{path}/photo_data.json', 'r', encoding='utf-8') as f:
    post_data = json.load(f)

images, exposures = [], []
for img_name in os.listdir(f'{path}/photos'):
    img = cv2.imread(f'{path}/photos/{img_name}')
    img = cv2.resize(img, (224, 224,))
    images.append(img)
    img_id = img_name.split('.')[0]
    photo_views = post_data[img_id]['photo_views']
    impressions_unique = post_data[img_id]['impressions_unique']
    r = photo_views / impressions_unique
    exposures.append(r)

median=np.median(exposures)
print(median)

exposures = [0 if exposure < np.median(exposures) else 1 for exposure in exposures]

X = np.array(images)/255.
y = np.array(exposures)

# 結合過採樣 欠採樣
from imblearn.combine import SMOTEENN

# 圖片數據攤平
X_flat = np.array([img.flatten() for img in X])

# 使用 SMOTEENN 進行過採樣及欠採樣
smoteenn = SMOTEENN()
X_resampled, y_resampled = smoteenn.fit_resample(X_flat, y)

# 數據恢復原狀
X_resampled = np.array([x.reshape(224, 224, 3) for x in X_resampled])

# 使用 resampled 數據劃分
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

from tensorflow.keras.utils import to_categorical

# 將標籤轉換為 one-hot 編碼形式
y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)

datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.1,
    channel_shift_range=0.1,
    shear_range=0.1,
    brightness_range=(0.5, 1.5),
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest'
)

train_datagen = datagen.flow(X_train, y_train, batch_size=16)
train_generator = iter(train_datagen)

from tensorflow.keras.applications import InceptionV3

base_model = InceptionV3(input_shape=(224, 224, 3), include_top=False, weights='imagenet')

for layer in base_model.layers:
    layer.trainable = False

model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Flatten())
model.add(Dense(512, activation='relu', kernel_regularizer=l2(0.001)))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu', kernel_regularizer=l2(0.001)))
model.add(Dropout(0.3))
model.add(Dense(2, activation='softmax'))

model.summary()

from keras.callbacks import ReduceLROnPlateau
from keras.optimizers import RMSprop
# optimizer = RMSprop(learning_rate=0.0001)
optimizer = Adam(learning_rate=0.001) 
# reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.00001)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(train_generator, epochs=32, validation_data=(X_test, y_test),
                    validation_freq=1, callbacks=[early_stopping])

model.save('FB_imagetest_model.h5')

import numpy as np
import cv2

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_image(model, img_path):
    preprocessed_img = preprocess_image(img_path)
    prediction = model.predict(preprocessed_img)
    result = np.argmax(prediction, axis=1)
    return result

# 使用預訓練模型對新圖片進行預測
new_image_path = 'path/to/your/new/image.jpg'
result = predict_image(model, new_image_path)

print(f"預測結果: {result}")
