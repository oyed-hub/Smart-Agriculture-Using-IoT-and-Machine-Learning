# 🌱 Smart Agriculture using AI & ML

An AI-driven Smart Agriculture system that provides **crop recommendations** and **irrigation guidance** based on environmental parameters such as temperature, humidity, soil moisture, and rainfall. The system helps farmers make **data-driven decisions** to improve productivity and promote sustainable agriculture.

---

## 📌 Features

- ✅ AI-based crop recommendation  
- 💧 Soil moisture–based irrigation suggestions  
- 📊 Data-driven decision support  
- 🖥️ Simple web-based user interface  
- ♻️ Supports sustainable farming  
- 💡 Low-cost and scalable (IoT & Weather API ready)

---

## 🧠 Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Machine Learning:** Scikit-learn (Random Forest, Decision Tree)  
- **Database:** MySQL (XAMPP)  
- **Tools:** VS Code, Jupyter Notebook  

---

## ⚙️ System Flow


**Input Parameters:**
- Temperature  
- Humidity  
- Soil Moisture  
- Rainfall  

---

## 📊 Model Performance

The performance of the machine learning models was evaluated using a test split of the dataset.

**Models Evaluated:**
- Decision Tree  
- Random Forest  
- Logistic Regression  

**Evaluation Metrics:**
- Accuracy  
- Precision  
- Recall  
- F1-Score  

**Experimental Results:**

| Model               | Test Accuracy | Precision | Recall | F1-Score |
|---------------------|---------------|-----------|--------|----------|
| Decision Tree       | ~82%          | ~0.81     | ~0.80  | ~0.80    |
| Random Forest       | **~88%**      | **~0.87** | **~0.86** | **~0.86** |
| Logistic Regression | ~76%          | ~0.75     | ~0.74  | ~0.74    |

> The Random Forest model achieved the best performance and was selected for the final system.  
> Results are based on experimental evaluation using a benchmark dataset. Real-world performance may vary.

---

## 📁 Project Structure

```bash
smart-agriculture/
│── app.py                  # Flask application entry point
│── evaluate_models.py      # Script to evaluate ML models
│── train_model.py          # Script to train and save the ML model
│── model/
│   └── trained_model.pkl   # Saved trained ML model
│── dataset/
│   └── agriculture_data.csv # Dataset used for training/testing
│── templates/
│   └── index.html          # Frontend HTML template
│── static/
│   ├── css/
│   │   └── styles.css      # CSS files
│   └── js/
│       └── script.js       # JavaScript files
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
```

---

## 🔮 Future Scope

- 🌐 Integrate real-time IoT sensors (soil moisture, temperature, humidity)  
- 🌦️ Connect weather APIs for live climate data  
- 📱 Develop a mobile application for farmers  
- 🗣️ Add multilingual support for regional languages  
- 📸 Implement crop disease detection using image processing  
- 🤖 Improve model accuracy with continuous retraining on new data    
- 🧠 Add fertilizer and pesticide dosage recommendations  

---

## 👨‍🌾 Target Users

- Farmers (small and medium-scale)  
- Agricultural students and researchers  
- NGOs working in rural development  
- Government agriculture departments  
- Smart farming and agri-tech developers  

