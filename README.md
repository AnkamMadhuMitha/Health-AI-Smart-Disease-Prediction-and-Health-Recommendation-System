# 🏥 Health AI - Smart Disease Prediction and Health Recommendation System

Health AI is a state-of-the-art, premium medical intelligence portal designed for patient screening and automated health planning. Powered by Machine Learning, the system assesses the risk of **8 major clinical diseases** based on patient health reports and generates highly customized, time-to-time diet schedules and daily exercise programs.

---

## 🚀 Key Features

* **🩺 8 Advanced Predictive Engines**:
  * **🩸 Diabetes Risk**: Evaluates pregnancies, glucose levels, blood pressure, insulin, BMI, and age.
  * **❤️ Heart Disease**: Assesses cardiovascular risks using age, cholesterol, resting blood pressure, chest pain classification, resting ECG, max heart rate, and stress test profiles.
  * **🧠 Parkinson's Disease**: Analyzes voice recordings utilizing 22 complex vocal acoustic frequencies and pitch instability indicators (Jitter, Shimmer, HNR, NHR).
  * **🧬 Chronic Kidney Disease (CKD)**: Evaluates renal health via urine specific gravity, albumin levels, red blood cells, serum creatinine, blood urea, and electrolyte levels.
  * **🧪 Liver Disease**: Screens for hepatobiliary issues utilizing age, gender, bilirubin, proteins, and liver enzymes (SGPT, SGOT, Alk Phos).
  * **🧴 Breast Cancer**: Evaluates malignancy risk by analyzing cell nuclei characteristics (radius, perimeter, area, texture, concavity).
  * **🧠 Stroke Risk**: Analyzes probabilities using hypertension history, heart disease history, glucose levels, smoking status, and BMI.
  * **🫁 Lung Cancer**: Examines environmental and lifestyle risk factors (smoking, alcohol, chronic cough, wheezing, fatigue).

* **🥗 Personalized Care Schedules**:
  * **Time-to-Time Diet Plans**: Step-by-step breakfast, lunch, snack, and dinner planning optimized for the patient's specific risk diagnosis.
  * **Exercise Schedules**: Clear morning and evening physical activity routines custom-tailored to aid clinical management.

* **📄 Premium PDF Clinical Reports**:
  * Auto-generates a creative PDF medical report featuring custom color themes, clean patient data summary tables, confidence badges, structured diets, and exercise timelines.

* **🛡️ Secure Patient Portal**:
  * Multi-user registration and encrypted authentication using SQLite.
  * **Prediction History**: A complete log of all past screenings, with search, filter, and PDF re-download options.

* **💎 High-Contrast Space-Dark UI**:
  * A beautiful, interactive dashboard styled with modern gradient typography (`#60A5FA` to `#34D399`), glassmorphism cards, hover effects, and responsive widget layout grids.

---

## 🛠️ Technology Stack

* **Front-End & Framework**: Streamlit (v1.40.1+)
* **Styling**: Vanilla CSS (embedded) & SVG Vector Graphics
* **Core Language**: Python (3.9+)
* **Machine Learning**: Scikit-Learn, Joblib, NumPy, Pandas
* **Report Generation**: FPDF
* **Database**: SQLite3

---

## 💻 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AnkamMadhuMitha/Health-AI-Smart-Disease-Prediction-and-Health-Recommendation-System.git
   cd Health-AI-Smart-Disease-Prediction-and-Health-Recommendation-System
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # For Windows PowerShell
   .venv\Scripts\Activate.ps1
   # For macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Web Application**:
   ```bash
   streamlit run app.py
   ```

---

## 🔬 How It Works

1. **Patient Authentication**: Log in or create a new account to keep your health data private and save your records.
2. **Select Assessment Type**: Navigate to the **Disease Prediction** screen and pick one of the 8 supported clinical screenings.
3. **Fill Parameters**: Enter details matching your clinical health report (pre-filled baseline averages are provided).
4. **Predict**: Click **Predict Risk** to run the Scikit-Learn model and render your **Confidence Score** and **AI Insights**.
5. **Care Plan Tabs**: Review time-to-time meals and exercises directly on screen.
6. **Export Report**: Download your professional PDF clinical summary with one click.

---

## ⚖️ Disclaimer

*This application is a machine learning prototype meant for informational screening and educational purposes. It does not constitute formal medical advice, diagnosis, or treatment. Always consult a qualified medical professional for health evaluations.*
