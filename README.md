# 🧠 NeuroGuard – Intelligent Facial Management System

**NeuroGuard** is an intelligent facial attendance and management system built using **Python** and **Flask**, with integrated facial recognition. It allows secure and automated attendance marking using real-time face data. The system uses OpenCV and face recognition models to detect and verify faces and record attendance in a database.

---

## 🚀 Features

- 📷 Real-time face capture for attendance
- 🧑‍💼 Admin panel with dashboard
- 📝 Attendance database with timestamp logging
- 🔐 Secure face registration with name labeling
- 🧠 Uses pre-trained face embeddings (`.pkl`)
- ☁️ Lightweight and fully local (can be deployed to the cloud)

---

## 🌐 Live Demo

🌐 `Coming Soon` (You can deploy it using Microsoft Azure, Render, or PythonAnywhere)

---

## 🛠️ Tech Stack

| Layer     | Technology        |
|-----------|-------------------|
| Frontend  | HTML, CSS         |
| Backend   | Python, Flask     |
| Database  | SQLite            |
| AI/ML     | OpenCV, face_recognition, NumPy |
| Packaging | Pickle (`.pkl`) for embeddings |

---

## 📁 Project Structure

NeuroGuard/
├── pycache/ # Compiled Python files
├── templates/ # HTML templates
│ ├── login.html
│ ├── dashboard.html
│ ├── attendance.html
│ ├── face_register.html
│ ├── face_recognize.html
│ └── setting.html
├── data/ # Face embeddings (ignored by Git)
│ ├── Pruthviraj_embeddings.pkl
│ └── admin1_embeddings.pkl
├── app.py # Main Flask application
├── attendance.py # Face recognition logic
├── attendance.db # SQLite database
├── .gitignore # Git ignore rules
├── requirements.txt # Python dependencies
└── README.md # This file


---

## ✅ Setup Instructions

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/Pruthviraj404/NeuroGuard.git
cd NeuroGuard



