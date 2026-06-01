# 🚗 Smart Parking Allocation System

## 📌 Project Overview

The Smart Parking Allocation System is a Streamlit-based web application that automates parking slot allocation and management. The system intelligently assigns parking spaces based on vehicle type and tracks vehicle entry and exit in real time.

This project helps reduce manual parking management efforts by providing an automated and user-friendly parking allocation solution.

---

## ✨ Features

### 🚘 Vehicle Entry Management

* Register incoming vehicles.
* Automatic parking slot allocation.
* Priority-based slot assignment.
* Prevent duplicate vehicle entries.

### 🚪 Vehicle Exit Management

* Vehicle checkout process.
* Automatic parking fee calculation.
* Parking duration tracking.
* Receipt generation.

### 🏢 Multi-Floor Parking Support

* 3-floor parking structure.
* 10 parking spots per floor.
* Different spot categories:

  * EV Parking
  * Compact Vehicle Parking
  * Regular Vehicle Parking

### 📊 Real-Time Monitoring

* Live parking occupancy status.
* Available and occupied slot visualization.
* Interactive parking lot map.

### 💾 Data Persistence

* Parking information stored using JSON.
* Automatic data loading and saving.
* Maintains parking state between application restarts.

---

## 🛠️ Technologies Used

* Python 3
* Streamlit
* JSON Database
* Datetime Module
* Math Module

---

## 📂 Project Structure

```text
smart-parking-system/
│
├── app.py
├── parking_data.json
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/smart-parking-system.git
cd smart-parking-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

## 🧠 Allocation Logic

### EV Vehicles

* Assigned to EV parking spots first.
* Falls back to regular spots if EV spots are unavailable.

### Compact Vehicles

* Assigned to Compact parking spots first.
* Falls back to regular spots if Compact spots are unavailable.

### Regular Vehicles

* Assigned directly to Regular parking spots.

---

## 💰 Parking Charges

| Vehicle Type      | Rate Per Hour |
| ----------------- | ------------- |
| EV                | ₹50           |
| Regular / Compact | ₹30           |

Minimum parking duration charged: 1 hour.

---

## 📷 Screenshots

### Dashboard

Add project screenshots here.

### Entry Gateway

Add entry form screenshot here.

### Exit Gateway

Add checkout screenshot here.

### Parking Lot Visualization

Add parking map screenshot here.

---

## 🚀 Future Enhancements

* QR Code Based Entry & Exit
* Online Payment Gateway
* Vehicle Reservation System
* Admin Dashboard
* Email Notifications
* AI-Based Slot Prediction
* Mobile Application Support
* Cloud Database Integration

---

## 👨‍💻 Author

**Veluvarthi Bhardwaj**

Smart Parking Allocation System Project

---

## 📄 License

This project is developed for educational and academic purposes.
