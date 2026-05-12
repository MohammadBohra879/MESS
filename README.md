# MESS
# 🏥 MESS – Medical Equipment Sharing System

<div align="center">

![MESS Logo](https://img.shields.io/badge/MESS-Medical%20Equipment%20Sharing%20System-blue)
![Django](https://img.shields.io/badge/Django-Framework-green)
![Python](https://img.shields.io/badge/Python-3.13-yellow)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Frontend-38B2AC)
![Status](https://img.shields.io/badge/Project-Active-success)

### A Smart Web Platform for Sharing Medical Equipment Efficiently

</div>

---

# 📌 Project Overview

MESS (Medical Equipment Sharing System) is a web-based platform designed to connect donors and requesters for medical equipment sharing.

The system helps hospitals, clinics, organizations, and individuals share unused or available medical equipment with people who urgently need it.

The platform simplifies:

* Equipment posting
* Equipment discovery
* Request management
* Approval/rejection workflow
* Distance-based equipment search
* Feedback and rating system
* Real-time equipment availability tracking

---

# 🎯 Problem Statement

Many medical devices remain unused while other hospitals or patients struggle to access them.

Traditional equipment sharing processes are:

* Slow
* Manual
* Non-transparent
* Difficult to manage
* Lack centralized communication

MESS solves this issue by providing a centralized digital platform where users can:

✅ Share medical equipment
✅ Request available equipment
✅ Track requests
✅ Manage approvals
✅ View nearby equipment
✅ Improve equipment utilization

---

# ✨ Key Features

## 👤 User Authentication

* User registration and login system
* Session-based authentication
* Profile management
* Secure access control

## 🩺 Equipment Management

* Add medical equipment
* Upload equipment images
* Update equipment availability
* Delete products
* Equipment detail pages

## 📍 Geolocation Support

* Automatic user location detection
* Distance calculation between donor and requester
* Reverse geocoding using latitude & longitude
* Nearby equipment discovery

## 📦 Product Listing System

* Responsive product cards
* Pagination support
* Product detail pages
* Equipment filtering

## 📨 Request Management

* Raise equipment requests
* Request confirmation system
* Approve/Reject workflow
* Request tracking
* Request status updates

## ⭐ Rating & Feedback System

* User feedback after product return
* Product ratings
* Average rating calculation
* Dynamic star rating UI

## 🖼 Media Upload System

* Upload images from device
* Store images in media folder
* Dynamic image rendering

## 📱 Responsive UI

* Mobile-friendly design
* Modern dashboard
* Tailwind CSS styling
* Interactive user experience

---

# 🏗️ System Architecture

The project follows a **3-Tier Architecture**.

## 1️⃣ Frontend Layer

Responsible for:

* User interface
* User interaction
* Dynamic rendering

### Technologies Used

* HTML5
* Tailwind CSS
* JavaScript

### Features

* Responsive UI
* Equipment cards
* Request interface
* Modal system
* Pagination
* Interactive forms

---

## 2️⃣ Backend Layer

Responsible for:

* Business logic
* Request processing
* Authentication
* Data handling

### Technology Used

* Django Framework

### Backend Functionalities

* User authentication
* Equipment management
* Request processing
* Rating calculations
* Distance calculations
* API handling
* Database operations
* Media handling

---

## 3️⃣ Database Layer

Responsible for secure data storage.

### Technologies Used

* MySQL (Development)
* PostgreSQL (Production Ready)

### Data Stored

* User details
* Equipment information
* Request records
* Ratings & feedback
* Geolocation details
* Availability status

---

# 🛠️ Technologies Used

| Technology              | Purpose             |
| ----------------------- | ------------------- |
| Python                  | Backend Programming |
| Django                  | Web Framework       |
| HTML5                   | Structure           |
| Tailwind CSS            | Styling             |
| JavaScript              | Interactivity       |
| MySQL                   | Database            |
| PostgreSQL              | Production Database |
| Geopy                   | Reverse Geolocation |
| Nominatim API           | Address Detection   |
| Browser Geolocation API | User Location       |

---

# 📂 Project Structure

```bash
MESS/
│
├── media/
│   └── equipment/
│
├── mess/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   ├── pre_sign/
│   │   └── sign_in/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
│
├── tamohdorg/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/MohammadBohra879/MESS.git
cd MESS
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install django mysqlclient pillow geopy
```

---

## 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6️⃣ Start Server

```bash
python manage.py runserver
```

---

# 🌐 Main Modules

| Module             | Description                 |
| ------------------ | --------------------------- |
| Authentication     | Login & Signup              |
| Profile System     | User profile management     |
| Equipment Module   | Add/Delete/View products    |
| Request Module     | Raise and manage requests   |
| Rating System      | Product feedback and rating |
| Geolocation System | Distance and area detection |
| Media Upload       | Image upload and rendering  |

---

# 🔄 Workflow of MESS

## Donor Workflow

1. Login/Register
2. Add medical equipment
3. Upload equipment image
4. Equipment becomes visible to users
5. Receive requests
6. Approve/Reject requests
7. Mark equipment status

## Requester Workflow

1. Browse available equipment
2. View equipment details
3. Check distance/location
4. Raise request
5. Wait for approval
6. Return equipment
7. Give feedback & rating

---

# 📷 Screens Included in Project

* Home Page
* Login & Signup
* Product Listing
* Product Detail Page
* Add Product Page
* Received Requests
* My Requests
* Feedback Page
* User Profile

---

# 🚧 Current Limitations

* No real-time notifications
* No chat system between users
* No AI recommendation system
* Basic admin panel
* Limited analytics dashboard

---

# 🚀 Future Scope

## Planned Improvements

* Real-time notifications
* AI-based equipment recommendation
* Chat/messaging system
* Advanced search & filtering
* Equipment tracking system
* QR code integration
* Mobile application
* Email/SMS notifications
* Admin analytics dashboard
* Cloud image storage

---

# 🔐 Security Features

* Session authentication
* Protected routes
* CSRF protection
* Secure media handling
* User authorization

---

# 📊 Project Highlights

✅ Responsive modern UI
✅ Full-stack Django project
✅ Real-world healthcare use case
✅ Image upload support
✅ Distance calculation feature
✅ Dynamic request management
✅ Rating & feedback system

---

# 👨‍💻 Developed By

## Mohammad Bohra

### B.Tech Student – Web Application Development

---

# 📬 Contact

## GitHub Repository

👉 [https://github.com/MohammadBohra879/MESS](https://github.com/MohammadBohra879/MESS)

---

# ⭐ Support

If you like this project, give it a ⭐ on GitHub.

---

<div align="center">

### 💙 MESS – Making Medical Equipment Sharing Easy & Efficient

</div>
