import cv2, os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l1, l2
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from scipy.stats import norm
import json

# path = '/content/drive/MyDrive/Colab Notebooks' # on colab
path = '.'  # on local side

with open(f'{path}/photo_data_new.json', 'r', encoding='utf-8') as f:
    post_data = json.load(f)

images, exposures = [], []
for img_name in os.listdir(f'{path}/photos'):
    img = cv2.imread(f'{path}/photos/{img_name}')
    img = cv2.resize(img, (75, 75,))
    images.append(img)
    img_id = img_name.split('.')[0]
#     exposures.append(post_data[img_id]['impressions_unique']/300000.)
    exposures.append(post_data[img_id]['impressions_unique'])

exposures = [0 if exposure < np.median(exposures) else 1 for exposure in exposures]


X = np.array(images)/255.
y = np.array(exposures)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.4,
    height_shift_range=0.4,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_datagen = datagen.flow(X_train, y_train, batch_size=24)
train_generator = iter(train_datagen)


from keras.applications import InceptionV3

base_model = InceptionV3(input_shape=(75, 75, 3), include_top=False, weights='imagenet')

for layer in base_model.layers:
    layer.trainable = False

model = Sequential()
model.add(base_model)
model.add(Flatten())
model.add(Dense(512, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))

model.summary()

learning_rate = 0.001 
optimizer = Adam(learning_rate=learning_rate) 
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(train_generator, epochs=32, validation_data=(X_test, y_test),
                    validation_freq=1)