import streamlit as st
from PIL import Image
import numpy as np
# Giả sử bạn có các hàm này trong chapter_ex.chapter9
from chapter_ex import chapter9 # Hoặc from chapter_ex.chapter9 import Erosion, Dilation, ...

# Cấu hình trang
st.set_page_config(page_title="Xử lý Ảnh - Chương 9", layout="wide", initial_sidebar_state="expanded")

st.title("🖼️ Bài tập Xử lý Ảnh - Chương 9")
st.markdown("Tải lên một ảnh màu để áp dụng các thuật toán hình thái học từ Chương 9 (thường xử lý trên ảnh nhị phân hoặc ảnh xám).")

# Upload image
uploaded_file = st.file_uploader("📂 Chọn một ảnh màu...", type=["jpg", "png", "jpeg", "tif"], label_visibility="collapsed", key="uploader_c9")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_gray = image.convert('L')
    img_gray_np = np.array(img_gray)
    input_image_np_c9 = img_gray_np 

    st.markdown("---")
    st.subheader("🎨 Ảnh Gốc và Ảnh Xám")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Ảnh màu đã tải lên", use_container_width=True, width=400)
    with col2:
        st.image(img_gray, caption="Phiên bản ảnh xám", use_container_width=True, width=400)

    st.markdown("---")
    st.header("Chương 9: Xử lý ảnh hình thái học")


    algorithms_c9 = ['Erosion', 'Dilation', 'OpeningClosing', 'Boundary', 'HoleFill', 'ConnectedComponent', 'CountRice']
    option_c9 = st.selectbox('Chọn thuật toán Chương 9:', algorithms_c9, key="c9_algo")
    st.info(f'Bạn đã chọn: **{option_c9}**')

    result_c9 = None
    ksize_c9 = 5

    if option_c9 in ['Erosion', 'Dilation', 'OpeningClosing', 'Boundary']:
        default_ksize_map = {'Erosion': 5, 'Dilation': 5, 'OpeningClosing': 5, 'Boundary': 5}
        default_ksize_val = st.session_state.get(f"c9_ksize_{option_c9}_val", default_ksize_map.get(option_c9, 5))
        ksize_c9 = st.slider(f"Kích thước kernel (số lẻ, cho {option_c9})",
                             min_value=1, max_value=51, value=default_ksize_val, step=2,
                             key=f"c9_ksize_{option_c9}")
        st.session_state[f"c9_ksize_{option_c9}_val"] = ksize_c9

    if option_c9 == 'Erosion':
        result_c9 = chapter9.Erosion(input_image_np_c9, ksize_c9)
    elif option_c9 == 'Dilation':
        result_c9 = chapter9.Dilation(input_image_np_c9, ksize_c9)
    elif option_c9 == 'OpeningClosing':
        result_c9 = chapter9.OpeningClosing(input_image_np_c9, ksize_c9)
    elif option_c9 == 'Boundary':
        result_c9 = chapter9.Boundary(input_image_np_c9, ksize_c9)
    elif option_c9 == 'HoleFill':
        result_c9 = chapter9.HoleFill(input_image_np_c9)
    elif option_c9 == 'ConnectedComponent':
        result_c9 = chapter9.ConnectedComponent(img_gray_np)
    elif option_c9 == 'CountRice':

        result_c9 = chapter9.CountRice(input_image_np_c9) 
    else:
        result_c9 = input_image_np_c9

    if result_c9 is not None:
        if isinstance(result_c9, tuple) and len(result_c9) > 0 and isinstance(result_c9[0], np.ndarray):
            st.image(result_c9[0], caption=f"Kết quả: {option_c9}", width=400)
        elif isinstance(result_c9, np.ndarray):
            st.image(result_c9, caption=f"Kết quả: {option_c9}", width=400)
    else:
        if not (option_c9 == 'ConnectedComponent' or option_c9 == 'CountRice'): 
            st.warning("Vui lòng chọn một thuật toán để xem kết quả hoặc kiểm tra hàm xử lý.")


else:
    st.info("👋 Chào mừng! Vui lòng tải lên một hình ảnh để bắt đầu với các thuật toán Chương 9.")