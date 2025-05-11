import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Xử lý ảnh số - ĐH SPKT",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #f5f5f5;
    }
    
    /* Title styles */
    h1 { /* Thay .stTitle bằng h1 để áp dụng cho markdown # */
        color: #1E3A8A;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 1rem 0; /* Giảm padding một chút nếu có logo phía trên */
    }
    
    /* Subtitle styles */
    .subtitle { /* Giữ lại nếu bạn có class này ở đâu đó, hoặc dùng h2, h3... */
        color: #4B5563;
        font-size: 1.5rem !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Info box styles - MODIFIED */
    .info-box {
        /* background-color: white; */ /* Đã loại bỏ để xóa nền trắng */
        padding: 2rem; /* Giữ lại padding để nội dung không sát lề */
        /* border-radius: 10px; */ /* Loại bỏ vì không còn nền hộp */
        /* box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); */ /* Loại bỏ vì không còn nền hộp */
        margin: 1rem 0; /* Giữ lại margin để tạo khoảng cách giữa các khối thông tin */
    }
    
    /* Highlight text */
    .highlight {
        color: #1E3A8A;
        font-weight: 600;
    }

    /* Button styles */
    .stButton > button {
        background-color: #1E3A8A;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Secondary button style - Cần đảm bảo áp dụng đúng */
    /* Streamlit có thể không dùng data-baseweb="button" cho tất cả các nút
       Nếu cần phân biệt nút secondary, có thể cần cách tiếp cận khác hoặc dùng key/class khi tạo nút */
    /* Ví dụ mục tiêu các nút không phải là primary */
    div[data-testid="stButton"] button:not(:hover):not([kind="primary"]):not([kind="form_submit"]) {
        background-color: #E5E7EB; /* Màu nền cho nút secondary */
        color: #1F2937; /* Màu chữ cho nút secondary */
    }
    div[data-testid="stButton"] button:not(:hover):not([kind="primary"]):not([kind="form_submit"]):hover {
        background-color: #D1D5DB; /* Màu nền khi hover nút secondary */
    }


    /* CSS cho các loại nút cụ thể dựa trên st.button(type=...) sẽ khó hơn vì Streamlit không thêm class theo type.
       Tuy nhiên, button mặc định đã được style ở trên.
       Nếu bạn tạo nút với st.button("Tên nút", type="secondary"), Streamlit có thể không có style riêng.
       Các style cho Success, Danger bên dưới là ví dụ nếu bạn có cách thêm class/aria-label đó. */

    /* Success button style (ví dụ nếu có class hoặc aria-label) */
    .stButton > button[aria-label="Success"] { /* Hoặc một class bạn tự thêm nếu có thể */
        background-color: #059669;
        color: white;
    }

    .stButton > button[aria-label="Success"]:hover {
        background-color: #047857;
    }

    /* Danger button style (ví dụ nếu có class hoặc aria-label) */
    .stButton > button[aria-label="Danger"] { /* Hoặc một class bạn tự thêm nếu có thể */
        background-color: #DC2626;
        color: white;
    }

    .stButton > button[aria-label="Danger"]:hover {
        background-color: #B91C1C;
    }
    </style>
""", unsafe_allow_html=True)

# --- Thêm Logo ---
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Logo_Tr%C6%B0%E1%BB%9Dng_%C4%90%E1%BA%A1i_H%E1%BB%8Dc_S%C6%B0_Ph%E1%BA%A1m_K%E1%BB%B9_Thu%E1%BA%ADt_TP_H%E1%BB%93_Ch%C3%AD_Minh.png/960px-Logo_Tr%C6%B0%E1%BB%9Dng_%C4%90%E1%BA%A1i_H%E1%BB%8Dc_S%C6%B0_Ph%E1%BA%A1m_K%E1%BB%B9_Thu%E1%BA%ADt_TP_H%E1%BB%93_Ch%C3%AD_Minh.png"

# Sử dụng HTML để căn giữa logo và điều chỉnh kích thước
# Bạn có thể điều chỉnh 'width: 200px;' thành kích thước mong muốn
logo_html = f"""
<div style="display: flex; justify-content: center; margin-bottom: 10px;">
    <img src="{logo_url}" alt="Logo Trường ĐH Sư Phạm Kỹ Thuật TP. Hồ Chí Minh" style="width: 200px; height: auto;">
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)
# --- Kết thúc thêm Logo ---

st.markdown("""
# 🎓 SẢN PHẨM CUỐI KỲ

### 🏫 ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP HỒ CHÍ MINH  
### 🖥️ KHOA CÔNG NGHỆ THÔNG TIN  

**Môn học:** Xử lý ảnh số  
**Giảng viên:** TS. Trần Tiến Đức  

**Sinh viên thực hiện:** 
- Nguyễn Văn Luân — 22110373  
- Đặng Huỳnh Sơn — 22110406  
""")

st.markdown("---")

st.markdown("""
    ## 📋 Tính năng chính
    
    1. **Nhận diện khuôn mặt từ Camera**
        - Nhận diện khuôn mặt thời gian thực
        - So sánh với cơ sở dữ liệu
        - Hiển thị thông tin nhận diện
    
    2. **Nhận diện khuôn mặt từ Video**
        - Xử lý video từ file
        - Nhận diện khuôn mặt trong video
        - Xuất kết quả

    3. **Chương 3**
    
    4. **Chương 4**
            
    5. **Chương 9**
            
    6. **Nhận diện trái cây**

    7. **Nhận diện biển báo**
    """)

st.markdown("---")

st.markdown("""
## 🚀 Hướng dẫn sử dụng

1. Chọn chế độ từ menu bên trái
2. Làm theo hướng dẫn trên từng trang
3. Đảm bảo camera hoạt động (nếu sử dụng tính năng camera)
4. Kiểm tra cơ sở dữ liệu khuôn mặt trước khi nhận diện
""")