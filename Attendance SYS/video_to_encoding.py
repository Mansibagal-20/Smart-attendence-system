import cv2
import face_recognition
import os
import pickle
import numpy as np

# --------------- Configuration ---------------
VIDEO_DIR = "known_videos"          # Folder containing .mp4 videos
OUTPUT_FILE = "encodings.pkl" # Output file for all encodings
SHOW_PREVIEW = True           # Set to True to view detected faces live
FRAME_SKIP = 10               # Process every 10th frame for efficiency
# ---------------------------------------------

known_encodings = []
known_names = []

# Get all video files in folder
videos = [v for v in os.listdir(VIDEO_DIR) if v.lower().endswith(".mp4")]

if not videos:
    print("⚠️ No .mp4 videos found in the 'known_videos/' folder.")
    exit()

for filename in videos:
    name = os.path.splitext(filename)[0]
    video_path = os.path.join(VIDEO_DIR, filename)
    print(f"\n[+] Processing video: {filename}")

    video = cv2.VideoCapture(video_path)
    frame_count = 0
    enc_list = []

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % FRAME_SKIP != 0:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for enc, (top, right, bottom, left) in zip(encodings, faces):
            enc_list.append(enc)

            if SHOW_PREVIEW:
                # Draw rectangles around faces for preview
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if SHOW_PREVIEW:
            cv2.imshow("Encoding Preview", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video.release()

    if len(enc_list) > 0:
        avg_enc = np.mean(enc_list, axis=0)
        known_encodings.append(avg_enc)
        known_names.append(name)
        print(f"✅ Encoded {name} ({len(enc_list)} samples)")
    else:
        print(f"⚠️ No face detected in {filename}")

cv2.destroyAllWindows()

# Save all encodings
if known_encodings:
    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump((known_encodings, known_names), f)
    print(f"\n✅ All encodings saved to '{OUTPUT_FILE}' for: {', '.join(known_names)}")
else:
    print("❌ No encodings generated. Check your videos or lighting.")
