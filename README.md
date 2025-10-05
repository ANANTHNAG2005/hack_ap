# 🌿 Crop Disease Detector & Organic Advisory System

A web-based application designed to help farmers and tribal communities detect crop diseases, get organic solutions, and access community knowledge—both online and offline.

---

## **Features**

### **1. Crop Disease Detection**
- Upload a plant image to detect disease using AI (PyTorch MobileNetV2 model).
- Instant disease prediction and display.

### **2. Organic Advisory**
- Provides disease-specific organic remedies.
- Integrates traditional knowledge with modern organic practices.

### **3. Seasonal Calendar**
- Month-wise preventive treatments for crops.
- Current month is displayed to avoid unnecessary information.

### **4. Weather Alerts**
- Location-based weather alerts using Open-Meteo API.
- Crop-specific advice for weather conditions (Rain, Clear, Thunderstorm, etc.).
- Offline fallback data for remote areas.

### **5. Video Tutorials**
- Step-by-step video guides for disease management.
- Can be filtered for the detected disease.
- Available offline from cached data.

### **6. Community Platform**
- Post and view messages about diseases and remedies.
- SQLite database stores community posts.

### **7. Success Stories**
- Log successful remedies and treatments.
- SQLite + SQLAlchemy used for tracking results.

### **8. Offline Mode**
- Caches recent remedies and tutorials for areas without internet.
- Works seamlessly for disease prediction, advisory, and tutorials.

---

## **Technologies Used**

- **Frontend:** HTML, CSS (`style.css`), JavaScript  
- **Backend:** FastAPI, SQLite, SQLAlchemy  
- **AI/ML:** PyTorch, Transformers pipeline (MobileNetV2)  
- **APIs:** Open-Meteo (weather), OpenStreetMap Nominatim (geocoding)  
- **Other Python Libraries:** Requests, SpeechRecognition, os, json, datetime  

---

## **Installation & Setup**

1. **Clone the repository**
```bash
git clone <https://github.com/ANANTHNAG2005/hack_ap/tree/main>
cd <backend>
Install Python dependencies
```
bash
Copy code
pip install fastapi uvicorn torch torchvision transformers requests SpeechRecognition sqlalchemy
Run the backend

bash
Copy code
uvicorn main:app --reload
Open the frontend

Open index.html in your browser.

Upload a plant image to detect disease.

Offline Mode
All recent remedies and tutorials are cached in offline_cache.json.

Works without an active internet connection.

Project Structure
pgsql
Copy code
project/
│
├─ frontend/
│  ├─ index.html
│  ├─ results.html
│  └─ style.css
│
├─ backend/
│  ├─ main.py
│  ├─ weather_alerts.py
│  ├─ seasonal_calendar.py
│  ├─ community.py
│  ├─ success_logs.py
│  ├─ tutorials.py
│  └─ offline_mode.py
   ├─ seasonal_calendar.json
│  ├─ labels.json
│  ├─ tutorials.json
│  └─ offline_cache.json

├─ databases/
│  ├─ community.db
│  └─ success_logs.db
│
└─ README.md


Future Improvements
1. Multi-language support for community and tutorials.
2. Mobile app version for easier offline access.
3. Real-time notifications for weather alerts and disease outbreaks.
