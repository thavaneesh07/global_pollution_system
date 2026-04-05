# 🌍 AI-Powered Global Pollution Analysis System

## 📌 Overview

The **AI-Powered Global Pollution Analysis System** is a full-stack web application that analyzes and predicts environmental pollution trends using real-world datasets. It supports both **air pollution** and **water quality analysis**, along with **forecasting** and an integrated **AI chatbot** for intelligent insights.

This system is designed to handle **dynamic datasets**, automatically detect their type, and update the dashboard in real-time — making it a powerful and flexible data analytics platform.

---

## 🚀 Features

### 🌫️ Air Pollution Analysis

* Detects AQI-related data automatically
* Displays top polluted regions
* Supports dynamic datasets with flexible column handling

### 🔮 Air Forecasting

* Time-series prediction using Linear Regression
* Automatically detects date & value columns
* Predicts future pollution trends

### 🌊 Water Quality Analysis

* Calculates average **pH** and **Dissolved Oxygen (DO)**
* Handles varied dataset formats dynamically
* Classifies water quality indicators

### 🔮 Water Forecasting

* Predicts future dissolved oxygen levels
* Uses historical yearly data
* Automatically adapts to dataset structure

### 📂 Smart Dataset Upload

* Upload any `.csv` dataset
* Automatically detects:

  * Air dataset 🌫️
  * Water dataset 🌊
* Updates dashboard instantly

### 🤖 AI Chatbot (Ollama Integration)

* Ask questions about uploaded dataset
* Generates intelligent insights using LLM
* Works locally via Ollama (LLaMA3)

### 📊 Interactive Dashboard

* Clean modern UI
* 4 main panels:

  * Air Analysis
  * Air Forecast
  * Water Analysis
  * Water Forecast
* Real-time updates after upload

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Pandas
* Scikit-learn
* Requests (for Ollama API)

### Frontend

* HTML, CSS, JavaScript
* Chart.js

### AI / LLM

* Ollama (LLaMA3 model)

---

## 📁 Project Structure

```
global_pollution_system/
│
├── backend/
│   └── app.py
│
├── frontend/
│   └── index.html
│
├── data/
│   ├── air_data.csv
│   ├── air_time.csv
│   └── water/
│       └── water_data.csv
│
├── notebooks/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone <your-repo-link>
cd global_pollution_system
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

Or manually:

```
pip install flask pandas scikit-learn requests flask-cors
```

---

### 3️⃣ Install Ollama (for Chatbot)

Download and install from:
👉 https://ollama.com

Run:

```
ollama run llama3
```

---

### 4️⃣ Run Backend

```
python backend/app.py
```

---

### 5️⃣ Run Frontend

```
cd frontend
python -m http.server 8000
```

---

### 6️⃣ Open in Browser

```
http://localhost:8000
```

---

## 📂 Supported Dataset Formats

### 🌫️ Air Dataset

Should contain:

* AQI values (e.g., "AQI Value")
* Country/Location
* Optional: Date for forecasting

### 🌊 Water Dataset

Should contain:

* pH Min / Max
* Dissolved Oxygen Min / Max
* Year (for forecasting)

👉 The system automatically detects column names even if formats vary.

---

## 🤖 Chatbot Usage

Ask questions like:

* "What is the average AQI?"
* "Which country is most polluted?"
* "Is the water safe?"
* "What trends do you see?"

---

## 🎯 Key Highlights

* ✅ Fully dynamic dataset handling
* ✅ Real-time dashboard updates
* ✅ Integrated AI chatbot
* ✅ Forecasting using machine learning
* ✅ Clean and modern UI

---

## 🚀 Future Improvements

* 🌍 Map-based visualization (Geo analytics)
* 📈 Advanced ML models (LSTM, ARIMA)
* ☁️ Cloud deployment
* 👤 User authentication system
* 📊 Multi-dataset comparison

---

## 👨‍💻 Author

**Thavaneesh D Shetty**

---

## 📜 License

This project is open-source and available under the MIT License.
