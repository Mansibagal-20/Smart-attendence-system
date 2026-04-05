import streamlit as st
import cv2
import face_recognition
import os  # ✅ Add this line
from datetime import datetime, time as dt_time
import pandas as pd
from pymongo import MongoClient
import schedule, time, threading
from streamlit_autorefresh import st_autorefresh
import numpy as np
import pickle
import tempfile


# ----------------- MongoDB Connection -----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["AttendanceDB"]
collection = db["Attendance"]

# ----------------- Load Known Encodings -----------------
ENCODING_FILE = "encodings.pkl"
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE, "rb") as f:
        known_encodings, known_names = pickle.load(f)
else:
    known_encodings, known_names = [], []

# ----------------- Attendance Function -----------------
def capture_and_mark(frame):
    now_time = datetime.now().time()
    start_time = dt_time(8, 30)
    end_time = dt_time(15, 30)

    if not (start_time <= now_time <= end_time):
        return []

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)
    marked_names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)
        best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else -1

        if best_match_index != -1 and matches[best_match_index]:
            name = known_names[best_match_index]
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time_now = now.strftime("%H:%M:%S")

            existing = collection.find_one({"Name": name, "Date": date})
            if not existing:
                collection.insert_one({"Name": name, "Date": date, "Time": time_now})
                marked_names.append(name)

    return marked_names

# ----------------- Helper to get frame -----------------
def get_current_frame():
    ret, frame = st.session_state.camera.read()
    return frame if ret else None

# ----------------- Scheduler -----------------
def run_scheduler():
    schedule.every(30).minutes.do(lambda: capture_and_mark(get_current_frame()))
    while True:
        schedule.run_pending()
        time.sleep(1)

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="AI/ML Face Attendance", layout="wide")
st.title("📸 Real-Time AI/ML Attendance System")
st_autorefresh(interval=90 * 1000, key="auto_refresh")

# Initialize camera
if "camera" not in st.session_state:
    st.session_state.camera = cv2.VideoCapture(0)

col1, col2 = st.columns(2)
FRAME_WINDOW = col1.image([])

# Start background scheduler
if "scheduler_started" not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    st.session_state.scheduler_started = True

# ----------------- Live Video Feed -----------------
col1.markdown("### 🎥 Live Camera Feed")
frame = get_current_frame()
if frame is not None:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    for (top, right, bottom, left), encoding in zip(faces, encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)
        name = "Unknown"
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

        # Draw rectangle & name label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 2, bottom - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# ----------------- Manual Capture Button -----------------
if col1.button("📷 Capture Attendance Now"):
    frame = get_current_frame()
    if frame is not None:
        names = capture_and_mark(frame)
        if names:
            st.success(f"✅ Attendance marked for: {', '.join(names)}")
        else:
            st.info("⚠️ No new attendance marked or outside hours.")

# ----------------- Attendance Records -----------------
with col2:
    st.subheader("📊 Attendance Records")
    data = list(collection.find({}, {"_id": 0}))
    if data:
        df = pd.DataFrame(data).sort_values(by=["Date", "Time"], ascending=[False, False])
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Attendance Summary by Date")
        summary = df.groupby("Date")["Name"].count().reset_index()
        st.bar_chart(summary.set_index("Date"))
    else:
        st.info("No attendance records yet.")
