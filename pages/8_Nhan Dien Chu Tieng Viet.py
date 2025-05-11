import streamlit as st
import tensorflow as tf
import os
import json
import cv2
import numpy as np
from tensorflow.keras.layers import Dense, LSTM, Reshape, BatchNormalization, Input, Conv2D, MaxPool2D, Lambda, Bidirectional, Add, Activation
from tensorflow.keras.models import Model
import tensorflow.keras.backend as K
from PIL import Image

# Cấu hình trang
st.set_page_config(page_title="Nhận diện chữ tiếng Việt", layout="wide", initial_sidebar_state="expanded")

st.title("🖼️ Nhận diện chữ tiếng Việt")
st.markdown("Tải lên một ảnh chứa văn bản tiếng Việt để nhận dạng.")

# Thiết lập đường dẫn
TRAIN_JSON = "labels.json"

# Đọc labels để lấy danh sách ký tự
with open(TRAIN_JSON, 'r', encoding='utf8') as f:
    train_labels = json.load(f)

# Tạo danh sách ký tự
char_list = set()
for label in train_labels.values():
    char_list.update(set(label))
char_list = sorted(char_list)
st.info(f"Số lượng ký tự: {len(char_list)}")
st.info(f"Danh sách ký tự: {''.join(char_list)}")

# Hằng số
MAX_WIDTH = 2167  # Chiều rộng tối đa cho ảnh

# Xây dựng model CRNN
inputs = Input(shape=(118,MAX_WIDTH,1))

# Block 1
x = Conv2D(64, (3,3), padding='same')(inputs)
x = MaxPool2D(pool_size=3, strides=3)(x)
x = Activation('relu')(x)
x_1 = x

# Block 2
x = Conv2D(128, (3,3), padding='same')(x)
x = MaxPool2D(pool_size=3, strides=3)(x)
x = Activation('relu')(x)
x_2 = x

# Block 3
x = Conv2D(256, (3,3), padding='same')(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x_3 = x

# Block 4
x = Conv2D(256, (3,3), padding='same')(x)
x = BatchNormalization()(x)
x = Add()([x,x_3])
x = Activation('relu')(x)
x_4 = x

# Block 5
x = Conv2D(512, (3,3), padding='same')(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x_5 = x

# Block 6
x = Conv2D(512, (3,3), padding='same')(x)
x = BatchNormalization()(x)
x = Add()([x,x_5])
x = Activation('relu')(x)

# Block 7
x = Conv2D(1024, (3,3), padding='same')(x)
x = BatchNormalization()(x)
x = MaxPool2D(pool_size=(3, 1))(x)
x = Activation('relu')(x)

x = MaxPool2D(pool_size=(3, 1))(x)
squeezed = Lambda(lambda x: K.squeeze(x, 1))(x)

blstm_1 = Bidirectional(LSTM(512, return_sequences=True, dropout=0.2))(squeezed)
blstm_2 = Bidirectional(LSTM(512, return_sequences=True, dropout=0.2))(blstm_1)

outputs = Dense(len(char_list)+1, activation='softmax')(blstm_2)

# Model cho inference
model = Model(inputs, outputs)

# Build model với một batch đầu vào
dummy_input = np.zeros((1, 118, MAX_WIDTH, 1))
model(dummy_input)

# Compile model với CTC loss
model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer='adam')

# Load weights
model.load_weights('model/model_checkpoint_weights.hdf5')

def preprocess_image(image):
    # Chuyển đổi PIL Image sang numpy array và xử lý
    img = np.array(image.convert('L'))
    height, width = img.shape
    img = cv2.resize(img,(int(118/height*width),118))
    height, width = img.shape

    # Đảm bảo giá trị đệm không âm
    padding_width = max(0, MAX_WIDTH - width)
    img = np.pad(img, ((0,0),(0, padding_width)), 'median')

    # Xử lý khi ảnh quá rộng
    if width > MAX_WIDTH:
        img = cv2.resize(img, (MAX_WIDTH, 118))

    img = cv2.GaussianBlur(img, (5,5), 0)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    img = np.expand_dims(img, axis=2)
    img = img/255.

    return np.expand_dims(img, axis=0)

def predict_text(image):
    # Tiền xử lý ảnh
    img = preprocess_image(image)

    # Dự đoán
    prediction = model.predict(img)
    out = K.get_value(K.ctc_decode(prediction, input_length=np.ones(prediction.shape[0])*prediction.shape[1], greedy=True)[0][0])

    # Chuyển đổi kết quả thành text
    pred = ""
    for p in out[0]:
        if int(p) != -1:
            pred += char_list[int(p)]

    return pred

# Upload image
uploaded_file = st.file_uploader("📂 Chọn một ảnh chứa văn bản tiếng Việt...", type=["jpg", "png", "jpeg", "tif"], label_visibility="collapsed")

if uploaded_file is not None:
    # Mở ảnh từ file
    image = Image.open(uploaded_file)

    # Hiển thị ảnh gốc
    st.subheader("🖼️ Ảnh gốc")
    st.image(image, use_container_width=True)

    # Chạy model dự đoán
    with st.spinner("🔍 Đang nhận diện văn bản..."):
        result = predict_text(image)
        
        # Hiển thị kết quả
        st.subheader("✅ Kết quả nhận diện")
        st.success(result)
else:
    st.info("👋 Chào mừng! Vui lòng tải lên một hình ảnh để bắt đầu nhận diện văn bản tiếng Việt.")
