# 📸 AI/ML-Based Facial Recognition Attendance System

An intelligent attendance management system that uses **computer vision** and **machine learning** to mark attendance automatically through facial recognition. Built using **Streamlit**, **OpenCV**, and **MongoDB**, this project offers a real-time attendance dashboard with automated and manual capture options.

---

## 🗂️ Project Structure

```
📁 Facial-Attendance-System/
│
├── 📁 known_videos/           # Folder containing known user videos for encoding
│
├── app.py                     # Main Streamlit application (attendance dashboard)
│
├── video_to_encoding.py       # Script to generate encodings.pkl from videos
│
├── encodings.pkl              # Stored face encodings and names
│
└── README.md                  # Project documentation
```

---

## 🚀 Features

✅ Real-time webcam-based face recognition  
✅ Automatic attendance marking (8:30 AM – 3:30 PM)  
✅ MongoDB integration for persistent record storage  
✅ Streamlit dashboard with live video and data visualization  
✅ Manual attendance button  
✅ Background scheduler (every 30 minutes)  
✅ Auto-refresh dashboard every 90 seconds  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/suryanshd49/Facial-attendance.git
cd Facial-attendance
```

### 2️⃣ Install Dependencies
Create a virtual environment (optional) and install required packages:
```bash
pip install -r requirements.txt
```

### 3️⃣ Start MongoDB
Ensure your local MongoDB server is running:
```bash
mongod
```

### 4️⃣ Generate Face Encodings
Place your known user videos inside the `known_videos/` folder and run:
```bash
python video_to_encoding.py
```
This will create an updated `encodings.pkl` file containing facial encodings.

### 5️⃣ Run Attendance App
```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. Loads known face encodings (`encodings.pkl`)  
2. Captures frames from webcam using OpenCV  
3. Detects and encodes faces with the `face_recognition` library  
4. Compares detected faces with known encodings  
5. Marks attendance in **MongoDB** (once per day)  
6. Displays results and charts in Streamlit dashboard  

---

## 🧩 Technologies Used

| Component | Technology |
|------------|-------------|
| UI Framework | Streamlit |
| Face Detection | face_recognition (dlib) |
| Image Processing | OpenCV |
| Data Storage | MongoDB |
| Scheduling | schedule + threading |
| Data Handling | Pandas |
| Auto Refresh | streamlit-autorefresh |

---

## 📊 Database Schema

**Database:** `AttendanceDB`  
**Collection:** `Attendance`

| Field | Type | Description |
|--------|------|-------------|
| `Name` | String | Recognized person’s name |
| `Date` | String | Date of attendance |
| `Time` | String | Time when attendance was marked |

---

## 📈 Dashboard View

- 🎥 **Live Camera Feed** (with bounding boxes and name labels)  
- 📷 **Manual Capture Button**  
- 📊 **Attendance Table** (sorted by Date & Time)  
- 📅 **Bar Chart Summary** (Attendance count by date)

---

## 🛠️ Future Enhancements

- Add login system for admin control  
- Cloud MongoDB (MongoDB Atlas) for remote access  
- Notifications for absentees  
- Multi-camera or IoT integration  
- Web deployment via Streamlit Cloud or Heroku  

---

## 👨‍💻 Authors

**Suryansh Desai (PRN-1032240037)**  
**Pranav Sawant (PRN-1032240050)**  
**Chinmay Narule (PRN-1032240046)**  
**Manasi Bagal (PRN-1262243457)**  

---

## 🏁 License

This project is open-source and available under the **MIT License**.
