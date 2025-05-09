import streamlit as st
from PIL import Image
import supervision as sv
from ultralytics import YOLO
import numpy as np

# Khởi tạo model
# Đảm bảo bạn có model nhận diện biển báo tại đường dẫn "model/road_sign_detection_model.onnx"
model = YOLO("model/road_sign_detection_model.onnx")  # Dùng "/" thay vì "\" cho tương thích hệ điều hành

# Tạo annotator
box_annotator = sv.BoxAnnotator(thickness=2) # Có thể điều chỉnh độ dày của bounding box
label_annotator = sv.LabelAnnotator(text_color=sv.Color.WHITE, text_scale=0.5, text_thickness=1) # Điều chỉnh màu sắc, kích thước chữ

# Giao diện Streamlit
st.title("🚦 Ứng dụng nhận diện biển báo giao thông")

# Nút upload ảnh
uploaded_file = st.file_uploader("📤 Tải lên một ảnh chứa biển báo", type=["jpg", "jpeg", "png"])

# Nếu người dùng đã upload
if uploaded_file is not None:
    # Mở ảnh từ file
    image = Image.open(uploaded_file).convert("RGB")

    # Hiển thị ảnh gốc
    st.subheader("🖼️ Ảnh gốc")
    st.image(image, use_container_width=True)

    # Chạy model dự đoán
    with st.spinner("🔍 Đang nhận diện biển báo..."):
        # result = model.predict(image, conf=0.25)[0] # Giữ nguyên hoặc điều chỉnh conf nếu cần
        # Sửa lỗi tiềm ẩn nếu model.predict trả về list rỗng hoặc đối tượng không mong muốn
        results = model.predict(image, conf=0.25)
        if not results or not results[0].boxes:
            st.warning("⚠️ Không phát hiện được biển báo nào trong ảnh với ngưỡng tin cậy hiện tại.")
            st.stop() # Dừng xử lý nếu không có kết quả
        
        result = results[0]
        detections = sv.Detections.from_ultralytics(result)

        # Lấy tên class từ model (nếu có và cần thiết cho labels)
        # Giả sử model.names chứa danh sách tên các loại biển báo
        labels = [
            f"{model.names[class_id]} {confidence:0.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence)
        ]

        # Annotate ảnh
        annotated_image = np.array(image.copy())  # Đổi sang mảng để supervision xử lý
        annotated_image = box_annotator.annotate(scene=annotated_image.copy(), detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)

    # Hiển thị ảnh kết quả
    st.subheader("✅ Ảnh sau khi nhận diện biển báo")
    st.image(annotated_image, use_container_width=True)

else:
    st.info("ℹ️ Vui lòng tải lên một ảnh để bắt đầu nhận diện biển báo.")