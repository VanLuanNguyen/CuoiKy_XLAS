import streamlit as st
import cv2
import time
import tempfile # Thêm thư viện tempfile
import os 
from utils.face_processing import process_frame


def show_video_page(detector, recognizer, database):
    """
    Hiển thị trang nhận diện khuôn mặt từ video, có xử lý xoay video.
    """
    st.markdown("## Nhận diện khuôn mặt từ Video")

    if detector is None or recognizer is None:
        st.error("Không thể tải mô hình. Vui lòng kiểm tra đường dẫn mô hình.")
        return

    video_file = st.file_uploader("Chọn file video", type=['mp4', 'avi', 'mov', 'mkv'])

    if video_file is not None:
        recognition_threshold = st.slider("Ngưỡng nhận diện (Video)", 0.0, 1.0, 0.4, key="video_threshold")

        if st.button("Bắt đầu xử lý Video", type="primary", key="process_video_button"):
            temp_file_path = ""
            rotation_angle = 0
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.' + video_file.name.split('.')[-1]) as tfile:
                    tfile.write(video_file.read())
                    temp_file_path = tfile.name

                cap = cv2.VideoCapture(temp_file_path)

                if not cap.isOpened():
                    st.error(f"Không thể mở file video: {video_file.name}.")
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    return

                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps == 0:
                    fps = 30
                    st.warning(f"Không đọc được FPS, sử dụng mặc định: {fps} FPS.")

                if total_frames <= 0:
                    st.error("Video không có frame hoặc không đọc được tổng số frame.")
                    cap.release()
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
                    return

                progress_bar = st.progress(0)
                status_text = st.empty()
                stats_container = st.container()
                col1, col2 = stats_container.columns(2)
                faces_detected_text = col1.empty()
                recognized_faces_text = col2.empty()
                stframe_placeholder = st.empty()

                frame_count = 0
                processed_display_count = 0 # Đếm số frame được hiển thị/xử lý chi tiết

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_count += 1

                    current_progress = frame_count / total_frames
                    progress_bar.progress(current_progress)
                    status_text.text(f"Đang xử lý: Frame {frame_count}/{total_frames}")

                    # Xử lý mỗi N frame để cải thiện hiệu suất (ví dụ: mỗi 3 frame)
                    # Hoặc xử lý tất cả frame nếu muốn (bỏ điều kiện if)
                    if frame_count % 3 == 0: # Chỉ xử lý và hiển thị mỗi 3 frame
                        processed_display_count += 1
                        processed_frame, results = process_frame(frame, detector, recognizer, database, recognition_threshold)

                        faces_detected_text.markdown(f"**Số khuôn mặt phát hiện (frame đang xử lý):** {len(results)}")
                        recognized_count = sum(1 for face in results if isinstance(face, dict) and face.get('name') != "Unknown" and face.get('name') is not None)
                        recognized_faces_text.markdown(f"**Số khuôn mặt nhận diện được (frame đang xử lý):** {recognized_count}")

                        try:
                            processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                            stframe_placeholder.image(processed_frame_rgb, channels="RGB", width=800)
                        except cv2.error as e:
                            st.warning(f"Lỗi chuyển đổi màu sắc frame {frame_count}: {e}. Bỏ qua hiển thị frame này.")
                    
                    # Delay nhỏ để UI có thể cập nhật
                    if fps > 0:
                        time.sleep(1 / (fps * 2)) # Tăng mẫu số để delay nhiều hơn, giảm tải
                    else:
                        time.sleep(0.02)

                cap.release()
                status_text.text(f"Hoàn tất xử lý {frame_count} frames (hiển thị/phân tích chi tiết {processed_display_count} frames).")
                st.success("Đã xử lý xong video!")
                progress_bar.progress(1.0)

            except Exception as e:
                st.error(f"Đã xảy ra lỗi trong quá trình xử lý video: {e}")
            finally:
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
    else:
        st.info("Vui lòng tải lên một file video để bắt đầu.")