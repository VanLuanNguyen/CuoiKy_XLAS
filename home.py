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
    .stTitle {
        color: #1E3A8A;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 2rem 0;
    }
    
    /* Subtitle styles */
    .subtitle {
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

    /* Secondary button style */
    .stButton > button[data-baseweb="button"] {
        background-color: #E5E7EB;
        color: #1F2937;
    }

    .stButton > button[data-baseweb="button"]:hover {
        background-color: #D1D5DB;
    }

    /* Success button style */
    .stButton > button[data-baseweb="button"][aria-label="Success"] {
        background-color: #059669;
        color: white;
    }

    .stButton > button[data-baseweb="button"][aria-label="Success"]:hover {
        background-color: #047857;
    }

    /* Danger button style */
    .stButton > button[data-baseweb="button"][aria-label="Danger"] {
        background-color: #DC2626;
        color: white;
    }

    .stButton > button[data-baseweb="button"][aria-label="Danger"]:hover {
        background-color: #B91C1C;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎓 SẢN PHẨM CUỐI KỲ")

# Thông tin trường
st.markdown('<p class="subtitle">🏫 ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP HỒ CHÍ MINH</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🖥️ KHOA CÔNG NGHỆ THÔNG TIN</p>', unsafe_allow_html=True)

# Thông tin môn học
with st.container():
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 📚 Thông tin môn học")
    st.markdown("**Môn học:** Xử lý ảnh số")
    st.markdown("**Giảng viên:** TS. Trần Tiến Đức")
    st.markdown("</div>", unsafe_allow_html=True)

# Thông tin sinh viên
with st.container():
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 👨‍🎓 Sinh viên thực hiện")
    st.markdown("""
    - **Nguyễn Văn Luân** — 22110373
    - **Đặng Huỳnh Sơn** — 22110406
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #6B7280;">© 2024 - Xử lý ảnh số - ĐH SPKT TP.HCM</p>', unsafe_allow_html=True)