import streamlit as st
import cv2
import time
import uuid
from utils.face_processing import process_frame


def show_camera_page(detector, recognizer, database):
    """
    Hiển thị trang nhận diện khuôn mặt từ camera với luồng webcam.

    Args:
        detector: Đối tượng FaceDetectorYN
        recognizer: Đối tượng FaceRecognizerSF
        database: Từ điển chứa các embedding khuôn mặt
    """
    st.markdown("## Nhận diện khuôn mặt từ Camera")

    if detector is None or recognizer is None:
        st.error("Không thể tải mô hình. Vui lòng kiểm tra đường dẫn mô hình.")
        return

    # Khởi tạo session_state nếu chưa có
    if 'camera_running' not in st.session_state:
        st.session_state.camera_running = False
    if 'cap' not in st.session_state:  # Để lưu đối tượng camera
        st.session_state.cap = None

    # Cài đặt Camera
    camera_options = ["Camera mặc định (0)"]
    for i in range(1, 5):  # Thêm các tùy chọn camera khác
        camera_options.append(f"Camera {i}")

    # Chỉ cho phép chọn camera khi camera chưa chạy
    selected_camera_option = st.selectbox(
        "Chọn Camera",
        camera_options,
        index=0, # Giá trị mặc định
        disabled=st.session_state.camera_running
    )
    try:
        camera_id_str = selected_camera_option.split("(")[1].split(")")[0]
        camera_id = int(camera_id_str)
    except (IndexError, ValueError):
        camera_id = camera_options.index(selected_camera_option)


    # Ngưỡng nhận diện
    recognition_threshold = st.slider(
        "Ngưỡng nhận diện", 0.0, 1.0, 0.4,
        disabled=st.session_state.camera_running
    )

    col1, col2 = st.columns(2)

    # Nút Bắt đầu Camera
    if not st.session_state.camera_running:
        if col1.button("Bắt đầu Camera", type="primary", key="start_camera_button"):
            st.session_state.camera_running = True
            try:
                st.session_state.cap = cv2.VideoCapture(camera_id)
                if not st.session_state.cap.isOpened():
                    st.error(f"Không thể mở camera {camera_id}. Hãy chọn camera khác hoặc kiểm tra lại.")
                    st.session_state.camera_running = False
                    st.session_state.cap = None
                else:
                    st.rerun() # Chạy lại script để cập nhật giao diện và bắt đầu vòng lặp camera
            except Exception as e:
                st.error(f"Lỗi khi mở camera {camera_id}: {e}")
                st.session_state.camera_running = False
                st.session_state.cap = None

    # Nút Dừng Camera
    else: # Nếu camera đang chạy
        if col2.button("Dừng Camera", type="secondary", key="stop_camera_button"):
            st.session_state.camera_running = False
            if st.session_state.cap is not None:
                st.session_state.cap.release()
                st.session_state.cap = None
            st.rerun() # Chạy lại script để dừng vòng lặp và cập nhật UI

    # Vòng lặp hiển thị camera và xử lý
    if st.session_state.camera_running and st.session_state.cap is not None and st.session_state.cap.isOpened():
        stframe = st.empty() # Placeholder cho khung hình camera
        stats_container = st.container()
        stat_col1, stat_col2 = stats_container.columns(2)
        faces_detected_text = stat_col1.empty()
        recognized_faces_text = stat_col2.empty()

        while st.session_state.camera_running: # Vòng lặp chính dựa vào session_state
            ret, frame = st.session_state.cap.read()
            if not ret:
                st.error("Không thể đọc khung hình từ camera. Đang dừng camera...")
                st.session_state.camera_running = False # Dừng nếu không đọc được frame
                if st.session_state.cap is not None:
                    st.session_state.cap.release()
                    st.session_state.cap = None
                st.rerun() # Chạy lại để cập nhật UI
                break # Thoát vòng lặp

            # Xử lý khung hình để phát hiện và nhận diện khuôn mặt
            processed_frame, results = process_frame(frame, detector, recognizer, database, recognition_threshold)

            # Cập nhật thống kê
            faces_detected_text.markdown(f"**Số khuôn mặt phát hiện:** {len(results)}")
            recognized_count = sum(1 for face in results if face.get('name', "Unknown") != "Unknown")
            recognized_faces_text.markdown(f"**Số khuôn mặt nhận diện được:** {recognized_count}")

            # Chuyển đổi sang RGB để hiển thị trong Streamlit
            try:
                processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                stframe.image(processed_frame_rgb, channels="RGB", width=800)
            except cv2.error as e:
                st.error(f"Lỗi chuyển đổi màu sắc khung hình: {e}")
                # Có thể hiển thị khung hình gốc nếu có lỗi
                # stframe.image(frame, channels="BGR", width=800)
                pass # Hoặc bỏ qua khung hình này

            time.sleep(0.01) # Độ trễ nhỏ để giảm tải CPU

        # Dọn dẹp khi vòng lặp kết thúc (camera_running = False)
        if st.session_state.cap is not None:
             st.session_state.cap.release()
             st.session_state.cap = None
        stframe.empty()
        faces_detected_text.empty()
        recognized_faces_text.empty()
        if not st.session_state.camera_running: # Chỉ hiển thị nếu thực sự dừng do người dùng hoặc lỗi
             st.success("Đã dừng camera.")
    elif not st.session_state.camera_running and st.session_state.cap is not None:
        # Trường hợp này đảm bảo camera được giải phóng nếu nó đã được khởi tạo nhưng không chạy
        st.session_state.cap.release()
        st.session_state.cap = None