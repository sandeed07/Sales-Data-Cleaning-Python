# 📊 Sales Data Cleaning & Interactive Dashboard

## 🚀 Project Overview

This project showcases how raw, messy sales data can be transformed into clean, actionable insights — followed by a modern, interactive dashboard experience. Built with **Python**, **Pandas**, **Streamlit**, and **Flask**, it's perfect for anyone looking to automate data workflows and visualize performance metrics dynamically.

---

## 🔑 Key Features

✅ **Data Cleaning**  
Automated script handles:
- Missing values
- Duplicate entries
- Inconsistent data types
- Standardized formats

🧮 **Data Transformation**  
Calculates:
- 📦 Total Sales Quantity  
- 💰 Total Revenue  
- 🛍️ Unique Products  

🔌 **Python API (Flask)**  
A lightweight API to serve cleaned data to any frontend (e.g. Next.js)

📈 **Interactive Dashboard (Streamlit)**  
Dynamic visualizations with filters and charts to explore sales performance

🖥️ **Next.js Frontend (Optional)**  
Sample frontend consuming the Flask API (React + Recharts)

---

## 🌐 Live Demo

🎯 **Try the interactive dashboard live:**  
👉 [Sales Performance Dashboard](https://sales-data-cleaning-python-cdpbtufudyoatkmxlxisnu.streamlit.app/)

---

## 📁 Project Structure

Sales-Data-Cleaning-Python/
├── app.py # Flask API (optional)
├── clean_data.py # Data cleaning logic
├── dashboard_app.py # Streamlit dashboard app
├── messy_sales_data.csv # Raw input data
├── cleaned_sales_data.csv # Cleaned output data
├── requirements.txt # Project dependencies
└── README.md


---

## ⚙️ How to Run Locally

### 📌 Prerequisites
- Python 3.8+
- pip

### 🔽 Clone or Download
```bash
git clone https://github.com/sandeed07/Sales-Data-Cleaning-Python.git
cd Sales-Data-Cleaning-Python

🧪 Create Virtual Environment
python -m venv venv

🔛 Activate the Environment
Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

📦 Install Dependencies
pip install -r requirements.txt

🧹 Run the Data Cleaning Script
python clean_data.py
### Generates cleaned_sales_data.csv from the messy input file.

🌐 Run the Flask API (Optional)
python app.py
Accessible at: http://localhost:5000

📊 Run the Streamlit Dashboard
streamlit run dashboard_app.py
Opens at: http://localhost:8501

---

🛠️ Technologies Used

🐍 Python – Core scripting

📊 Pandas – Data cleaning & manipulation

🔥 Flask – Backend API

🎨 Streamlit – Interactive dashboard

📈 Plotly Express – Dynamic charting

🌐 Next.js + Recharts – Example frontend integration (optional)

---

📬 Contact

📇 Connect on LinkedIn: https://www.linkedin.com/in/sandeedhasnain/

Sandeed Hasnain

Feel free to reach out if you have questions, ideas, or want to collaborate!



