import streamlit as st
from PIL import Image
import numpy as np
# Giả sử bạn có các hàm này trong chapter_ex.chapter3
from chapter_ex import chapter3 # Hoặc from chapter_ex.chapter3 import Negative, Logarit, ...

# Cấu hình trang
st.set_page_config(page_title="Xử lý Ảnh - Chương 3", layout="wide", initial_sidebar_state="expanded")

st.title("🖼️ Bài tập Xử lý Ảnh - Chương 3")
st.markdown("Tải lên một ảnh màu để áp dụng các thuật toán xử lý ảnh từ Chương 3.")

# Upload image
uploaded_file = st.file_uploader("📂 Chọn một ảnh màu...", type=["jpg", "png", "jpeg", "tif"], label_visibility="collapsed", key="uploader_c3")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_gray = image.convert('L')
    img_gray_np = np.array(img_gray)
    img_color_np = np.array(image.convert('RGB'))

    st.markdown("---")
    st.subheader("🎨 Ảnh Gốc và Ảnh Xám")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Ảnh màu đã tải lên", use_container_width=True,width=400)
    with col2:
        st.image(img_gray, caption="Phiên bản ảnh xám", use_container_width=True, width=400)

    st.markdown("---")
    st.header("Chương 3: Các thuật toán xử lý điểm và lọc không gian")

    algorithms_c3 = ['Negative', 'Logarit', 'Power', 'PiecewiseLinear', 'Histogram', 'HistEqual',
                     'HistEqualColor', 'LocalHist', 'HistStat', 'BoxFilter', 'SmoothingGauss',
                     'Threshold', 'MedianFilter', 'Sharpen', 'UnSharpMasking', 'Gradient']
    option_c3 = st.selectbox('Chọn thuật toán Chương 3:', algorithms_c3, key="c3_algo")
    st.info(f'Bạn đã chọn: **{option_c3}**')

    result_c3 = None
    input_image_np_c3 = img_gray_np
    if option_c3 == 'HistEqualColor':
        input_image_np_c3 = img_color_np

    if option_c3 == 'Negative':
        result_c3 = chapter3.Negative(input_image_np_c3)
    elif option_c3 == 'Logarit':
        result_c3 = chapter3.Logarit(input_image_np_c3)
    elif option_c3 == 'Power':
        gamma = st.slider("Gamma (cho Power)", 0.1, 10.0, 5.0, key="c3_gamma")
        result_c3 = chapter3.Power(input_image_np_c3, gamma)
    elif option_c3 == 'PiecewiseLinear':
        result_c3 = chapter3.PiecewiseLinear(input_image_np_c3)
    elif option_c3 == 'Histogram':
        result_c3_data = chapter3.Histogram(input_image_np_c3)
        if isinstance(result_c3_data, np.ndarray):
            result_c3 = result_c3_data
        else:
            fig_hist = chapter3.PlotHistogram(input_image_np_c3) 
            if fig_hist:
                st.pyplot(fig_hist)
            else:
                st.write("Không thể hiển thị histogram.")
            result_c3 = None
    elif option_c3 == 'HistEqual':
        result_c3 = chapter3.HistEqual(input_image_np_c3)
    elif option_c3 == 'HistEqualColor':
        result_c3 = chapter3.HistEqualColor(img_color_np)
    elif option_c3 == 'LocalHist':
        result_c3 = chapter3.LocalHist(input_image_np_c3)
    elif option_c3 == 'HistStat':
        result_c3 = chapter3.HistStat(input_image_np_c3)
    elif option_c3 == 'BoxFilter':
        result_c3 = chapter3.BoxFilter(input_image_np_c3)
    elif option_c3 == 'SmoothingGauss':
        result_c3 = chapter3.SmoothingGauss(input_image_np_c3)
    elif option_c3 == 'Threshold':
        result_c3 = chapter3.Threshold(input_image_np_c3)
    elif option_c3 == 'MedianFilter':
        result_c3 = chapter3.MedianFilter(input_image_np_c3)
    elif option_c3 == 'Sharpen':
        result_c3 = chapter3.Sharpen(input_image_np_c3)
    elif option_c3 == 'UnSharpMasking':
        result_c3 = chapter3.UnSharpMasking(input_image_np_c3)
    elif option_c3 == 'Gradient':
        result_c3 = chapter3.Gradient(input_image_np_c3)
    else:
        result_c3 = input_image_np_c3

    if result_c3 is not None:
        if option_c3 == 'Histogram' and not isinstance(result_c3, np.ndarray):
            pass
        else:
            st.image(result_c3, caption=f"Kết quả: {option_c3}", width=400)
    elif option_c3 != 'Histogram':
        st.warning("Vui lòng chọn một thuật toán hợp lệ hoặc kiểm tra lại hàm xử lý.")

else:
    st.info("👋 Chào mừng! Vui lòng tải lên một hình ảnh để bắt đầu với các thuật toán Chương 3.")