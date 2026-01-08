
# AGENTIC-AI BASED PROJECT


# 🌱 **AI Plant Health Detection System**

*A Computer Vision + Weather Intelligence + Agentic AI based Crop Health Assistant*

---

## 📌 **Project Overview**

This project is an **AI-powered plant disease detection system** that helps farmers and users identify plant leaf diseases using **image analysis**.
Users upload a leaf image → YOLOv8 model detects disease → Weather API gives local conditions → Agentic AI generates treatment recommendations → Results saved in history.

The system is designed as a complete pipeline with:
✔ Machine Learning
✔ Flask Backend
✔ MongoDB Database
✔ Streamlit Frontend
✔ Google Login
✔ Weather API Integration
✔ Intelligent AI Recommendation Agent

---

## 🎯 **Features**

### 🔍 **1. Plant Disease Detection (YOLOv8)**

* Trained custom dataset from Roboflow
* Detects multiple leaf diseases
* Shows bounding boxes + confidence

### ☁ **2. Weather Integration**

* Fetches current and forcast weather data
* Uses temperature, humidity, rainfall to generate better disease diagnosis

### 🤖 **3. AI Recommendation System**

* Provides summarized & full treatment advice
* Considers local weather + disease type
* Uses LLM + agentic pipeline

### 🖼 **4. Image Upload**

* Upload from Camera or File
* Backend stores processed image
* Frontend shows annotated image

### 🔐 **5. Login System (Google OAuth)**

* Users can login with Google
* Or use app without login
* Logged-in users get history & sync

### 📜 **6. History Management**

* View previously scanned images
* View AI summaries and full recommendations
* Delete history items

### 🗃 **7. MongoDB Database**

* Stores user details
* Stores image results
* Collections:
  * **image**
  * **report**
  * **users**
  * **history**

---

## 🧱 **Tech Stack**

### 🔧 **Backend**

* Flask
* Python
* ultralytics (YOLOv8)
* MongoDB
* Pydantic
* python-dotenv

### 🎨 **Frontend**

* Streamlit
* HTML/CSS (custom styling)

### ☁ **APIs**

* OpenWeather API
* Custom Flask endpoints

## 🚀 **How It Works (Flow)**

### **1️⃣ User uploads a leaf image**

→ via Streamlit

### **2️⃣ Image sent to FastAPI backend**

→ `/predict` endpoint handles processing

### **3️⃣ YOLOv8 model detects disease**

→ bounding boxes + labels

### **4️⃣ Weather API called**

→ gives humidity/temp/rainfall

### **5️⃣ Agentic AI generates advice**

→ summary + full paragraph

### **6️⃣ Results returned to frontend**

→ Image + detection + weather + AI advice

### **7️⃣ If logged in → Save to MongoDB**

→ image + results stored in history

---

## 🛠 **Setup Instructions**

### **Backend Setup**

```bash
cd SERVER
pip install -r requirements.txt
python main.py
```

Add `.env` file:

```
MONGO_URI=your_mongodb_uri
OPENWEATHER_API_KEY=key
SECRET_KEY=random_key
GOOGLE_CLIENT_ID=xxxx
GOOGLE_CLIENT_SECRET=xxxx
```

---

### **Frontend Setup**

```bash
cd CLIENT
streamlit run app.py
```

---

## 🧪 **Future Enhancements**

* Fertilizer recommendation system
* Crop yield prediction
* Offline mobile app version
* Better history filters
* Better model's prediction
* Make this more agentic
* Adding login system with personlaized recommendation based on   the history of the user.
---

