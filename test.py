import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# 載入預訓練模型
model = load_model('mnist_cnn_model.h5')  # 替換成你的模型路徑


def preprocess_digit(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 轉換為灰階圖像
    image = cv2.resize(image, (28, 28))  # 調整大小為28x28
    image = image / 255.0  # 標準化
    image = np.expand_dims(image, axis=0)  # 增加批次維度
    image = np.expand_dims(image, axis=-1)  # 增加通道維度
    return image


# 讀取圖像
image = cv2.imread(r"C:\Users\user\Desktop\STlight.RptWordAcceptance\photo\UploadFiles\LightLog\404838_2.jpg")

# 轉換為灰階圖像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 應用二值化處理
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# 找到輪廓
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 過濾並顯示輪廓
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / float(h)

    # 根據尺寸和形狀過濾
    if 0.2 < aspect_ratio < 1.2 and 15 < w < 200 and 15 < h < 200:
        roi = image[y:y+h, x:x+w]

        # 預處理數位圖像
        processed_digit = preprocess_digit(roi)

        # 預測數位
        prediction = model.predict(processed_digit)
        digit = np.argmax(prediction)

        # 顯示識別結果
        cv2.putText(image, str(digit), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# 使用 matplotlib 顯示標註結果
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
