import streamlit as st
from PIL import Image
import numpy as np
# Giả sử bạn có các hàm này trong chapter_ex.chapter4
from chapter_ex import chapter4 # Hoặc from chapter_ex.chapter4 import Spectrum, ...

# Cấu hình trang
st.set_page_config(page_title="Xử lý Ảnh - Chương 4", layout="wide", initial_sidebar_state="expanded")

st.title("🖼️ Bài tập Xử lý Ảnh - Chương 4")
st.markdown("Tải lên một ảnh màu để áp dụng các thuật toán xử lý ảnh từ Chương 4 (thường xử lý trên ảnh xám).")

# Upload image
uploaded_file = st.file_uploader("📂 Chọn một ảnh màu...", type=["jpg", "png", "jpeg", "tif"], label_visibility="collapsed", key="uploader_c4")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_gray = image.convert('L')
    img_gray_np = np.array(img_gray)

    st.markdown("---")
    st.subheader("🎨 Ảnh Gốc và Ảnh Xám")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Ảnh màu đã tải lên", use_container_width=True, width=400)
    with col2:
        st.image(img_gray, caption="Phiên bản ảnh xám", use_container_width=True, width=400)

    st.markdown("---")
    st.header("Chương 4: Xử lý ảnh trong miền tần số")

    algorithms_c4 = ['Spectrum', 'FrequencyFilter', 'DrawNotchRejectFilter', 'RemoveMoire']
    option_c4 = st.selectbox('Chọn thuật toán Chương 4:', algorithms_c4, key="c4_algo")
    st.info(f'Bạn đã chọn: **{option_c4}**')

    result_c4 = None
    if option_c4 == 'Spectrum':
        result_c4 = chapter4.Spectrum(img_gray_np)
    elif option_c4 == 'FrequencyFilter':
        result_c4 = chapter4.FrequencyFilter(img_gray_np)
    elif option_c4 == 'DrawNotchRejectFilter': 
        result_c4 = chapter4.ApplyNotchFilter(img_gray_np) 
    elif option_c4 == 'RemoveMoire':
        result_c4 = chapter4.RemoveMoire(img_gray_np)
    else:
        result_c4 = img_gray_np

    if result_c4 is not None:
        st.image(result_c4, caption=f"Kết quả: {option_c4}", width=400)
    else:
        st.warning("Vui lòng chọn một thuật toán để xem kết quả hoặc kiểm tra hàm xử lý.")

else:
    st.info("👋 Chào mừng! Vui lòng tải lên một hình ảnh để bắt đầu với các thuật toán Chương 4.")