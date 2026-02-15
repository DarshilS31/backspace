Got it ✅
Here is **ONLY the README.md content** — clean and ready to paste.

---

# 🍽️ Smart Mess QR System

A FastAPI-based Smart Mess Management System built for hackathon demonstration.

This system allows students to:

* ✅ Login using Student ID
* ✅ Pre-book meals
* ✅ Scan QR (hostel button) to mark attendance
* ✅ View booking history
* ✅ View dashboard summary

---

## 🚀 Tech Stack

* **Backend:** FastAPI
* **Database:** SQLite (SQLAlchemy ORM)
* **Frontend:** HTML + TailwindCSS
* **Server:** Uvicorn

---

## 📂 Project Structure

```
smart-mess-system/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── scheduler.py
│
├── routers/
│   ├── auth.py
│   ├── booking.py
│   ├── scan.py
│   └── dashboard.py
│
├── services/
│   ├── validation.py
│   ├── meal_logic.py
│   ├── capacity.py
│   └── time_utils.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── prebook.html
│   ├── scan.html
│   ├── history.html
│   └── profile.html
│
└── mess.db
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy python-multipart
```

---

### 3️⃣ Run Server

```bash
uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

### 4️⃣ Open Frontend

Open:

```
templates/login.html
```

Or run with Live Server.

---

## 👨‍🎓 Demo Student IDs

| ID | Name  | Year | Hostel |
| -- | ----- | ---- | ------ |
| 1  | Rahul | 1    | H1     |
| 2  | Aman  | 1    | H1     |
| 3  | Priya | 2    | H2     |
| 4  | Karan | 2    | H2     |
| 5  | Sneha | 3    | H3     |

---

## 🎬 Demo Flow

1. Login with Student ID
2. Pre-book meal
3. Go to Scan page
4. Click Hostel button
5. Attendance marked
6. View updated history

---

## 🛠 Features

* Duplicate booking prevention
* Double scan prevention
* Year eligibility validation
* Capacity control
* Auto demo data seeding

---

## 👨‍💻 Author

Darshil Sharma,Anshuman Garg,Harsh Agrawal
Team Backspace
Hackathon Project 🚀

---

Done.
