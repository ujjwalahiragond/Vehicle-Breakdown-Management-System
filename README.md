# 🚗 Vehicle Breakdown Assistance Management System

<p align="center">
  <strong>A Django-based web application for managing vehicle breakdown and roadside assistance services.</strong>
</p>

<p align="center">
  Request Assistance • Manage Mechanics • Track Requests • Manage Payments
</p>

---

## 📌 About the Project

**Vehicle Breakdown Assistance Management System** is a web-based application developed using **Python and Django** to simplify and manage roadside vehicle assistance services.

The system allows customers to request assistance for vehicle breakdowns, enables administrators to manage customers, requests and mechanics, provides request tracking, and supports service payments and mechanic salary management.

The main goal of this project is to provide a **simple, organized, and efficient platform for managing roadside assistance operations**.

---

## 🎯 Project Objectives

- Provide an easy platform for customers to request roadside assistance.
- Manage customer assistance requests efficiently.
- Assign and manage mechanics for service requests.
- Track the progress of assistance requests.
- Manage mechanic schedules and availability.
- Manage service payments and generate receipts.
- Manage monthly mechanic salary payments.
- Collect customer ratings and feedback.
- Provide centralized administration of roadside assistance services.

---

## ✨ Key Features

### 👤 Customer Module

- Customer Registration
- Customer Login and Logout
- Request Vehicle Assistance
- Enter Vehicle Details
- Select Required Service
- Submit Breakdown Location
- Track Assistance Request
- View Request Status
- Service Payment
- Payment Receipt
- Customer Rating
- Customer Feedback

### 🔧 Mechanic Management

- Add and Manage Mechanics
- Mechanic Specialization
- Mechanic Availability
- Assign Mechanics to Requests
- Mechanic Scheduling
- Manage Assigned Jobs
- Monthly Salary Payment Management
- Salary Payment Receipt

### 🚨 Assistance Request Management

- Create Assistance Requests
- Assign Mechanics
- Manage Request Status
- Track Service Progress
- Manage Completed Requests
- Manage Cancelled Requests
- Customer Feedback Management

### 💳 Payment Management

- Service Amount Management
- Payment Status
- Payment Method
- Payment ID
- Payment Date
- Service Payment Receipt
- Monthly Mechanic Salary Payments
- Salary Payment Receipt

### 📊 Admin Management

- Customer Management
- Mechanic Management
- Assistance Request Management
- Service Management
- Schedule Management
- Payment Management
- Salary Payment Management
- Request Status Management

---

## 🚘 Available Services

| Service | Description |
|---|---|
| 🔧 Mechanical Assistance | General vehicle mechanical support |
| 🔋 Battery Assistance | Battery-related roadside support |
| 🛞 Tyre Assistance | Tyre-related roadside assistance |
| ⛽ Fuel Assistance | Emergency fuel support |
| 🚚 Towing Service | Vehicle towing assistance |
| 🔐 Lockout Assistance | Vehicle lockout support |
| 🌡️ Engine Overheating | Engine overheating assistance |
| 🚑 Accident Assistance | Roadside accident support |
| ⛽ Fuel Delivery | Emergency fuel delivery |
| 🚨 Emergency Roadside | Emergency roadside assistance |
| 🔍 Vehicle Inspection | Basic vehicle inspection |
| 🛠️ Roadside Support | General roadside support |

---

## 🔄 System Workflow

```text
                    CUSTOMER
                       │
                       ▼
                Register / Login
                       │
                       ▼
             Request Assistance
                       │
                       ▼
          Select Service & Vehicle
                       │
                       ▼
             Assistance Request
                       │
                       ▼
              Mechanic Assignment
                       │
                       ▼
              Mechanic Schedule
                       │
                       ▼
               Service Progress
                       │
                       ▼
              Service Completed
                       │
                       ▼
                Payment & Receipt
                       │
                       ▼
               Rating & Feedback
🛠️ Technology Stack
Frontend
HTML5
CSS3
JavaScript
Backend
Python
Django
Database
SQLite
Development Tools
Visual Studio Code
Git
GitHub
⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/ujjwalahiragond/Vehicle-Breakdown-Management-System.git
2. Navigate to the Project
cd Vehicle-Breakdown-Management-System
3. Navigate to the Django Project Directory
cd vehiclebreakdownmanagementsystem
4. Create a Virtual Environment
python -m venv djenv
5. Activate the Virtual Environment

Windows:

djenv\Scripts\activate
6. Install Django
pip install django
7. Apply Database Migrations
python manage.py migrate
8. Start the Development Server
python manage.py runserver
9. Open the Application
http://127.0.0.1:8000/
🖥️ Application Screenshots

The following screenshots demonstrate the major modules and functionality of the Vehicle Breakdown Assistance Management System.

🏠 Home Page

🔐 Login & Registration

👤 Customer Dashboard

🚨 Request Assistance

📍 Request Tracking

📊 Admin Dashboard

💳 Payment Management

🔧 Mechanic Management

📄 Mechanic Payment Receipt

📍 Location

🛠️ Services

ℹ️ About

🔐 Security & Development Practices

The project follows Django-based development practices including:

Django Authentication
CSRF Protection
Django ORM
Database Migrations
.gitignore configuration
Separation of application logic and templates

Sensitive and unnecessary development files such as:

SQLite database files
Python cache files
Virtual environments
ZIP archives

are excluded from the Git repository using .gitignore.

🚀 Future Enhancements

The project can be further enhanced with:

📍 Real-time GPS tracking
🗺️ Google Maps integration
📱 Mobile application
🔔 SMS and Email notifications
💳 Online payment gateway
🤖 AI-based vehicle issue assistance
🔧 Smart mechanic recommendation
📡 Real-time mechanic location tracking
📊 Advanced analytics dashboard
🔐 Enhanced role-based access control
🎓 Academic Project

This project was developed as an academic project for B.Sc. Computer Science to demonstrate practical knowledge of:

Python Programming
Django Web Development
Database Management
CRUD Operations
Authentication
Web Application Development
Payment Management
Scheduling
Git and GitHub
👩‍💻 Developer

Ujjwala Hiragond

B.Sc. Computer Science

GitHub:

https://github.com/ujjwalahiragond

📄 License

This project is developed for academic and educational purposes.
