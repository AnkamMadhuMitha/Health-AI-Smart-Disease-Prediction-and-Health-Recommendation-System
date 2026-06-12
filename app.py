import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sqlite3
from datetime import datetime

from auth import register_user, login_user, user_exists
from recommendation import get_recommendation
from report_generator import generate_report
from database import save_prediction, get_prediction_history

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Health AI",
    page_icon="🏥",
    layout="wide"
)

# ----------------------------
# CUSTOM PREMIUM CSS
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Force premium dark space theme */
[data-testid="stAppViewContainer"] {
    background-color: #0b0f19 !important;
    background-image: radial-gradient(at 0% 0%, #1e293b 0, transparent 50%), 
                      radial-gradient(at 50% 0%, #0f172a 0, transparent 50%), 
                      radial-gradient(at 100% 0%, #0b0f19 0, transparent 50%) !important;
    color: #F8FAFC !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #E2E8F0;
    font-weight: 500;
}

/* Custom premium card containers */
.premium-card {
    background: rgba(30, 41, 59, 0.7) !important;
    backdrop-filter: blur(12px);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin-bottom: 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: #F8FAFC !important;
}
.premium-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px -15px rgba(59, 130, 246, 0.25);
    border-color: rgba(96, 165, 250, 0.35) !important;
}

.premium-title {
    color: #F8FAFC !important;
    font-weight: 700;
    font-size: 1.25rem;
    margin-bottom: 8px;
}

.premium-desc {
    color: #94A3B8 !important;
    font-size: 0.88rem;
    line-height: 1.5;
}

/* Button enhancements */
.stButton>button {
    background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    height: 48px;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px -3px rgba(59, 130, 246, 0.4) !important;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #059669 100%) !important;
    box-shadow: 0 10px 20px -5px rgba(59, 130, 246, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    font-weight: 800;
    color: #38BDF8 !important;
}
[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

/* Recommendation display card */
.rec-card {
    background-color: rgba(15, 23, 42, 0.4) !important;
    border-left: 5px solid #34D399 !important;
    padding: 16px;
    border-radius: 12px;
    margin-top: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* High Risk / Low Risk highlights */
.high-risk-badge {
    background-color: rgba(239, 68, 68, 0.15) !important;
    color: #F87171 !important;
    padding: 8px 16px;
    border-radius: 9999px;
    font-weight: 700;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    display: inline-block;
    margin-bottom: 12px;
    font-size: 0.9rem;
}

.low-risk-badge {
    background-color: rgba(16, 185, 129, 0.15) !important;
    color: #34D399 !important;
    padding: 8px 16px;
    border-radius: 9999px;
    font-weight: 700;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    display: inline-block;
    margin-bottom: 12px;
    font-size: 0.9rem;
}

/* Make container border style match dark theme */
[data-testid="stContainerBorder"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background-color: rgba(30, 41, 59, 0.4) !important;
    border-radius: 16px !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# SESSION STATE
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ----------------------------
# LOGIN / REGISTER
# ----------------------------
if not st.session_state.logged_in:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 15px;'>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="url(#logo-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 54px; height: 54px; margin-right: 12px;">
                    <defs>
                        <linearGradient id="logo-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#60A5FA" />
                            <stop offset="100%" stop-color="#34D399" />
                        </linearGradient>
                    </defs>
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                </svg>
                <h1 style='background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.2rem; font-weight: 800; margin: 0;'>Health AI</h1>
            </div>
            <p style='color: #94A3B8; font-size: 1.1rem; font-weight: 500;'>Smart Disease Prediction and Health Recommendation System</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            menu = st.radio(
                "Account Options",
                ["Login", "Register"],
                horizontal=True
            )

            if menu == "Register":
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Create Account"):
                    if user_exists(username):
                        st.error("Username already exists")
                    else:
                        register_user(username, password)
                        st.success("Registration Successful! Please switch to Login.")
            else:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Login"):
                    user = login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid Credentials")
    st.stop()

# ----------------------------
# LOAD MODELS & SCALERS
# ----------------------------
@st.cache_resource
def load_ml_models():
    models = {}
    scalers = {}
    
    # Diabetes
    models["diabetes"] = joblib.load("models/diabetes_model.pkl")
    scalers["diabetes"] = joblib.load("models/diabetes_scaler.pkl")
    
    # Heart
    models["heart"] = joblib.load("models/heart_model.pkl")
    scalers["heart"] = joblib.load("models/heart_scaler.pkl")
    
    # Parkinson's
    models["parkinsons"] = joblib.load("models/parkinsons_model.pkl")
    scalers["parkinsons"] = joblib.load("models/parkinsons_scaler.pkl")
    
    # Stroke
    models["stroke"] = joblib.load("models/stroke_model.pkl")
    scalers["stroke"] = joblib.load("models/stroke_scaler.pkl")
    
    # Kidney
    models["kidney"] = joblib.load("models/ckd_model.pkl")
    scalers["kidney"] = joblib.load("models/ckd_scaler.pkl")
    
    # Liver
    models["liver"] = joblib.load("models/liver_model.pkl")
    scalers["liver"] = joblib.load("models/liver_scaler.pkl")
    
    # Lung Cancer
    models["lung"] = joblib.load("models/lung_cancer_model.pkl")
    scalers["lung"] = joblib.load("models/lung_cancer_scaler.pkl")
    
    # Breast Cancer
    models["breast"] = joblib.load("models/breast_cancer_model.pkl")
    scalers["breast"] = joblib.load("models/breast_cancer_scaler.pkl")
    
    return models, scalers

models, scalers = load_ml_models()

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
st.sidebar.markdown(f"""
    <div style='display: flex; flex-direction: column; align-items: center; text-align: center; padding: 10px 0;'>
        <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 5px;'>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="url(#logo-grad-side)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 32px; height: 32px; margin-right: 8px;">
                <defs>
                    <linearGradient id="logo-grad-side" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#60A5FA" />
                        <stop offset="100%" stop-color="#34D399" />
                    </linearGradient>
                </defs>
                <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
            <h2 style='color: #F8FAFC; font-weight: 800; font-size: 1.6rem; margin: 0;'>Health AI</h2>
        </div>
        <p style='color: #94A3B8; font-size: 0.85rem; margin-top: 5px;'>Logged in as: <b>{st.session_state.username}</b></p>
    </div>
    <hr style='border-color: #334155; margin: 10px 0;'/>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation Menu",
    [
        "Dashboard",
        "Disease Prediction",
        "Prediction History"
    ]
)

st.sidebar.markdown("<hr style='border-color: #334155; margin: 20px 0;'/>", unsafe_allow_html=True)
if st.sidebar.button("🔓 Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# ----------------------------
# DASHBOARD PAGE
# ----------------------------
if page == "Dashboard":
    st.markdown(f"""
        <h1 style='background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.2rem; margin-bottom: 5px;'>📊 Smart Health Dashboard</h1>
        <p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 25px;'>Welcome back, <b>{st.session_state.username}</b>! Here is a summary of the medical analytics portal.</p>
    """, unsafe_allow_html=True)

    # Calculate predictions count
    history = get_prediction_history(st.session_state.username)
    predictions_count = len(history)
    
    # Metric rows
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='premium-card' style='text-align: center; min-height: 180px;'>
                <div style='color: #60A5FA; font-size: 2.5rem; margin-bottom: 10px;'>📊</div>
                <div style='font-size: 0.9rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;'>Total Predictions Run</div>
                <div style='font-size: 2.2rem; font-weight: 800; color: #60A5FA; margin-top: 5px;'>{predictions_count}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class='premium-card' style='text-align: center; min-height: 180px;'>
                <div style='color: #34D399; font-size: 2.5rem; margin-bottom: 10px;'>🧬</div>
                <div style='font-size: 0.9rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;'>Supported Diseases</div>
                <div style='font-size: 2.2rem; font-weight: 800; color: #34D399; margin-top: 5px;'>8</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class='premium-card' style='text-align: center; min-height: 180px;'>
                <div style='color: #FBBF24; font-size: 2.5rem; margin-bottom: 10px;'>⚡</div>
                <div style='font-size: 0.9rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;'>AI Engine Status</div>
                <div style='font-size: 2.2rem; font-weight: 800; color: #34D399; margin-top: 5px;'>Online & Ready</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin-top: 20px; margin-bottom: 15px;'>🧬 Supported Clinical Predictions</h3>", unsafe_allow_html=True)
    
    # Grid of supported models
    grid1, grid2, grid3, grid4 = st.columns(4)
    
    with grid1:
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>🩸 Diabetes</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Predicts diabetes mellitus risk based on diagnostic measurements like glucose, BMI, and family pedigree.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>🧠 Parkinson's</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Uses vocal frequencies and speech acoustic parameters to identify Parkinsonian motor fluctuations.</div>
            </div>
        """, unsafe_allow_html=True)

    with grid2:
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>❤️ Heart Disease</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Assesses cardiovascular risk utilizing age, chest pain type, cholesterol, resting ECG, and slopes.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>🧴 Breast Cancer</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Analyzes cell nuclei characteristics (radius, perimeter, area, texture) to predict malignancy.</div>
            </div>
        """, unsafe_allow_html=True)

    with grid3:
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>🧬 Kidney Disease</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Screens for Chronic Kidney Disease using specific gravity, hemoglobin, albumin, and urea stats.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>🧠 Stroke Risk</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Identifies stroke probability using hypertension status, age, heart disease history, and average glucose levels.</div>
            </div>
        """, unsafe_allow_html=True)

    with grid4:
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>🧪 Liver Disease</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Examines liver enzymes, proteins, and bilirubin levels to forecast hepatobiliary abnormalities.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='premium-card' style='min-height: 210px;'>
                <div class='premium-title' style='font-size: 1.15rem;'>🫁 Lung Cancer</div>
                <div class='premium-desc' style='font-size: 0.85rem;'>Analyzes patient habits (smoking, alcohol) and clinical signs (wheezing, chronic cough) to screen risk.</div>
            </div>
        """, unsafe_allow_html=True)

# ----------------------------
# DISEASE PREDICTION PAGE
# ----------------------------
elif page == "Disease Prediction":
    st.markdown("""
        <h1 style='background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.2rem; margin-bottom: 5px;'>🩺 Disease Risk Assessment</h1>
        <p style='color: #64748B; font-size: 1.1rem; margin-bottom: 25px;'>Select a target disease and enter details to trigger an AI predictive risk analysis.</p>
    """, unsafe_allow_html=True)

    disease = st.selectbox(
        "Select Target Disease",
        [
            "Diabetes",
            "Heart Disease",
            "Parkinson's",
            "Kidney Disease",
            "Liver Disease",
            "Breast Cancer",
            "Stroke",
            "Lung Cancer"
        ]
    )

    st.markdown("<hr style='border-color: #E2E8F0; margin: 15px 0 25px 0;'/>", unsafe_allow_html=True)

    # Variable definition for results
    predicted_result = None
    risk_score = 0
    recommendation = ""
    pdf_ready = False

    # --------------------------------
    # 1. DIABETES FORM
    # --------------------------------
    if disease == "Diabetes":
        st.subheader("🩸 Diabetes Risk Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            pregnancies = st.slider("Pregnancies", 0, 20, 0)
            glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=100)
            blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=80)
        with col2:
            insulin = st.number_input("Insulin Level (mu U/ml)", min_value=0, max_value=900, value=80)
            bmi = st.number_input("BMI (Body Mass Index)", min_value=0.0, max_value=70.0, value=24.5)
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=25)

        if st.button("🔍 Predict Diabetes Risk"):
            # Set clinical average defaults for advanced parameters removed from UI
            skin_thickness = 20.0
            dpf = 0.5
            input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
            input_scaled = scalers["diabetes"].transform(input_data)
            
            pred_class = models["diabetes"].predict(input_scaled)[0]
            prob = models["diabetes"].predict_proba(input_scaled)[0]
            
            predicted_result = "High Risk" if pred_class == 1 else "Low Risk"
            risk_score = int(prob[1] * 100)
            recommendation = get_recommendation("Diabetes", pred_class)
            pdf_ready = True

    # --------------------------------
    # 2. HEART DISEASE FORM
    # --------------------------------
    elif disease == "Heart Disease":
        st.subheader("❤️ Heart Disease Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=50)
            sex = st.selectbox("Sex", ["Male", "Female"])
            cp_type = st.selectbox("Chest Pain Type", [
                "No Pain (Asymptomatic)", 
                "Mild / Atypical Pain", 
                "Non-Cardiac / General Chest Pain", 
                "Severe / Typical Angina Pain"
            ])
            resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0, max_value=240, value=120)
            cholesterol = st.number_input("Serum Cholesterol (mg/dl)", min_value=0, max_value=600, value=200)
        with col2:
            fasting_bs = st.selectbox("Is Fasting Blood Sugar High? (>120 mg/dL)", ["No", "Yes"])
            resting_ecg = st.selectbox("Resting ECG Results", [
                "Normal", 
                "Minor Abnormality (ST Wave)", 
                "Major Abnormality / Muscle Thickening (LVH)"
            ])
            max_hr = st.number_input("Max Heart Rate Achieved (bpm)", min_value=60, max_value=220, value=150)
            exercise_angina = st.selectbox("Chest Pain During Exercise", ["No", "Yes"])
            oldpeak = st.number_input("ECG Stress Test score (ST Depression)", min_value=-3.0, max_value=10.0, value=1.0, step=0.1)
            st_slope = st.selectbox("Peak Exercise ST Segment Slope", [
                "Normal / Upsloping", 
                "Flat / Borderline", 
                "Downsloping / Abnormal"
            ])

        if st.button("🔍 Predict Heart Disease Risk"):
            # Encodings
            sex_encoded = 1 if sex == "Male" else 0
            
            # Map simplified chest pain labels
            cp_map = {
                "No Pain (Asymptomatic)": 0, 
                "Mild / Atypical Pain": 1, 
                "Non-Cardiac / General Chest Pain": 2, 
                "Severe / Typical Angina Pain": 3
            }
            cp_encoded = cp_map[cp_type]
            
            fasting_bs_encoded = 1 if fasting_bs == "Yes" else 0
            
            # Map simplified ECG results
            ecg_map = {
                "Major Abnormality / Muscle Thickening (LVH)": 0, 
                "Normal": 1, 
                "Minor Abnormality (ST Wave)": 2
            }
            ecg_encoded = ecg_map[resting_ecg]
            
            angina_encoded = 1 if exercise_angina == "Yes" else 0
            
            # Map simplified ST segment slope
            slope_map = {
                "Downsloping / Abnormal": 0, 
                "Flat / Borderline": 1, 
                "Normal / Upsloping": 2
            }
            slope_encoded = slope_map[st_slope]
            
            input_data = np.array([[
                age, sex_encoded, cp_encoded, resting_bp, cholesterol, 
                fasting_bs_encoded, ecg_encoded, max_hr, angina_encoded, oldpeak, slope_encoded
            ]])
            
            input_scaled = scalers["heart"].transform(input_data)
            
            pred_class = models["heart"].predict(input_scaled)[0]
            prob = models["heart"].predict_proba(input_scaled)[0]
            
            predicted_result = "High Risk" if pred_class == 1 else "Low Risk"
            risk_score = int(prob[1] * 100)
            recommendation = get_recommendation("Heart Disease", pred_class)
            pdf_ready = True

    # --------------------------------
    # 3. PARKINSON'S FORM
    # --------------------------------
    elif disease == "Parkinson's":
        st.subheader("🧠 Parkinson's Disease Voice Acoustic Assessment")
        st.info("👋 Enter the patient's vocal frequency and acoustic measurements from their report below:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fo = st.number_input("Average Vocal Frequency / Pitch (Fo)", value=197.07, format="%.5f")
            fhi = st.number_input("Maximum Vocal Frequency (Fhi)", value=233.93, format="%.5f")
            flo = st.number_input("Minimum Vocal Frequency (Flo)", value=78.33, format="%.5f")
            jitter_percent = st.number_input("Voice Pitch Instability (Jitter %)", value=0.00281, format="%.5f")
            jitter_abs = st.number_input("Voice Pitch Instability (Jitter Abs)", value=0.00001, format="%.5f")
            rap = st.number_input("Rapid Amplitude Perturbation (RAP)", value=0.00118, format="%.5f")
            ppq = st.number_input("Period Perturbation Quotient (PPQ)", value=0.00153, format="%.5f")
        with col2:
            ddp = st.number_input("Average Absolute Difference of Jitter (DDP)", value=0.00355, format="%.5f")
            shimmer = st.number_input("Voice Amplitude Instability (Shimmer)", value=0.0119, format="%.5f")
            shimmer_db = st.number_input("Voice Amplitude Instability (Shimmer dB)", value=0.107, format="%.5f")
            apq3 = st.number_input("Amplitude Perturbation (APQ3)", value=0.00554, format="%.5f")
            apq5 = st.number_input("Amplitude Perturbation (APQ5)", value=0.0072, format="%.5f")
            apq = st.number_input("Amplitude Perturbation (APQ)", value=0.01006, format="%.5f")
            dda = st.number_input("Average Absolute Difference of Shimmer (DDA)", value=0.0166, format="%.5f")
        with col3:
            nhr = st.number_input("Noise-to-Harmonics Ratio (NHR)", value=0.00263, format="%.5f")
            hnr = st.number_input("Harmonics-to-Noise Ratio (HNR)", value=26.37, format="%.5f")
            rpde = st.number_input("Recurrence Period Density Entropy (RPDE)", value=0.322, format="%.5f")
            dfa = st.number_input("Signal Fractal Exponent (DFA)", value=0.825, format="%.5f")
            spread1 = st.number_input("Vocal Spread Parameter 1", value=-6.966, format="%.5f")
            spread2 = st.number_input("Vocal Spread Parameter 2", value=0.1755, format="%.5f")
            d2 = st.number_input("Correlation Dimension (D2)", value=1.721, format="%.5f")
            ppe = st.number_input("Pitch Period Entropy (PPE)", value=0.12, format="%.5f")

        if st.button("🔍 Predict Parkinson's Risk"):
            input_data = np.array([[
                fo, fhi, flo, jitter_percent, jitter_abs, rap, ppq, ddp,
                shimmer, shimmer_db, apq3, apq5, apq, dda, nhr, hnr,
                rpde, dfa, spread1, spread2, d2, ppe
            ]])
            input_scaled = scalers["parkinsons"].transform(input_data)
            
            pred_class = models["parkinsons"].predict(input_scaled)[0]
            prob = models["parkinsons"].predict_proba(input_scaled)[0]
            
            predicted_result = "High Risk" if pred_class == 1 else "Low Risk"
            risk_score = int(prob[1] * 100)
            recommendation = get_recommendation("Parkinson's", pred_class)
            pdf_ready = True

    # -------------------------    elif disease == "Kidney Disease":
        st.subheader("🧬 Chronic Kidney Disease (CKD) Screening")
        st.info("👋 Enter the patient's clinical kidney function metrics from their report below:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=50)
            bp = st.number_input("Blood Pressure (mm Hg)", min_value=40, max_value=200, value=80)
            sg = st.selectbox("Urine Specific Gravity", [1.005, 1.010, 1.015, 1.020, 1.025], index=3) # index of 1.020
            al = st.slider("Urine Albumin Level", 0, 5, 0)
            su = st.slider("Urine Sugar Level", 0, 5, 0)
            rbc = st.selectbox("Red Blood Cells (Urine)", ["normal", "abnormal"], index=0)
            pc = st.selectbox("Pus Cell (Urine)", ["normal", "abnormal"], index=0)
            pcc = st.selectbox("Pus Cell Clumps (Urine)", ["notpresent", "present"], index=0)
        with col2:
            ba = st.selectbox("Bacteria in Urine", ["notpresent", "present"], index=0)
            bgr = st.number_input("Blood Glucose Random (mg/dL)", value=120.0)
            bu = st.number_input("Blood Urea (mg/dL)", value=40.0)
            sc = st.number_input("Serum Creatinine (mg/dL)", value=1.2)
            sod = st.number_input("Blood Sodium Level (mEq/L)", value=138.0)
            pot = st.number_input("Blood Potassium Level (mEq/L)", value=4.5)
            hemo = st.number_input("Hemoglobin (gms)", value=15.0)
            pcv = st.number_input("Packed Cell Volume (%)", min_value=9, max_value=54, value=44)
        with col3:
            wc = st.number_input("White Blood Cell Count", min_value=2200, max_value=26400, value=7800)
            rc = st.number_input("Red Blood Cell Count (millions)", min_value=2.1, max_value=8.0, value=5.2, step=0.1)
            htn = st.selectbox("Hypertension (High BP)", ["no", "yes"], index=0)
            dm = st.selectbox("Diabetes Mellitus", ["no", "yes"], index=0)
            cad = st.selectbox("Coronary Artery Disease", ["no", "yes"], index=0)
            appet = st.selectbox("Appetite (Good/Poor)", ["good", "poor"], index=0)
            pe = st.selectbox("Pedal Edema (Foot Swelling)", ["no", "yes"], index=0)
            ane = st.selectbox("Anemia", ["no", "yes"], index=0)

        if st.button("🔍 Predict Kidney Disease Risk"):
            # Mappings for Kidney disease categorical strings
            rbc_encoded = 1 if rbc == "normal" else 0
            pc_encoded = 1 if pc == "normal" else 0
            pcc_encoded = 1 if pcc == "present" else 0
            ba_encoded = 1 if ba == "present" else 0
            htn_encoded = 1 if htn == "yes" else 0
            
            # dm classes: '\tno':0, '\tyes':1, ' yes':2, 'no':3, 'yes':4
            dm_encoded = 4 if dm == "yes" else 3
            # cad classes: '\tno':0, 'no':1, 'yes':2
            cad_encoded = 2 if cad == "yes" else 1
            
            appet_encoded = 1 if appet == "poor" else 0
            pe_encoded = 1 if pe == "yes" else 0
            ane_encoded = 1 if ane == "yes" else 0
            
            # String categoricals like pcv, wc, rc mapped to their label encoding values
            pcv_map = {'\t43': 0, '\t?': 1, '14': 2, '15': 3, '16': 4, '17': 5, '18': 6, '19': 7, '20': 8, '21': 9, '22': 10, '23': 11, '24': 12, '25': 13, '26': 14, '27': 15, '28': 16, '29': 17, '30': 18, '31': 19, '32': 20, '33': 21, '34': 22, '35': 23, '36': 24, '37': 25, '38': 26, '39': 27, '40': 28, '41': 29, '42': 30, '43': 31, '44': 32, '45': 33, '46': 34, '47': 35, '48': 36, '49': 37, '50': 38, '51': 39, '52': 40, '53': 41, '54': 42, '9': 43}
            wc_map = {'\t6200': 0, '\t8400': 1, '\t?': 2, '10200': 3, '10300': 4, '10400': 5, '10500': 6, '10700': 7, '10800': 8, '10900': 9, '11000': 10, '11200': 11, '11300': 12, '11400': 13, '11500': 14, '11800': 15, '11900': 16, '12000': 17, '12100': 18, '12200': 19, '12300': 20, '12400': 21, '12500': 22, '12700': 23, '12800': 24, '13200': 25, '13600': 26, '14600': 27, '14900': 28, '15200': 29, '15700': 30, '16300': 31, '16700': 32, '18900': 33, '19100': 34, '21600': 35, '2200': 36, '2600': 37, '26400': 38, '3800': 39, '4100': 40, '4200': 41, '4300': 42, '4500': 43, '4700': 44, '4900': 45, '5000': 46, '5100': 47, '5200': 48, '5300': 49, '5400': 50, '5500': 51, '5600': 52, '5700': 53, '5800': 54, '5900': 55, '6000': 56, '6200': 57, '6300': 58, '6400': 59, '6500': 60, '6600': 61, '6700': 62, '6800': 63, '6900': 64, '7000': 65, '7100': 66, '7200': 67, '7300': 68, '7400': 69, '7500': 70, '7700': 71, '7800': 72, '7900': 73, '8000': 74, '8100': 75, '8200': 76, '8300': 77, '8400': 78, '8500': 79, '8600': 80, '8800': 81, '9000': 82, '9100': 83, '9200': 84, '9300': 85, '9400': 86, '9500': 87, '9600': 88, '9700': 89, '9800': 90, '9900': 91}
            rc_map = {'\t?': 0, '2.1': 1, '2.3': 2, '2.4': 3, '2.5': 4, '2.6': 5, '2.7': 6, '2.8': 7, '2.9': 8, '3': 9, '3.0': 10, '3.1': 11, '3.2': 12, '3.3': 13, '3.4': 14, '3.5': 15, '3.6': 16, '3.7': 17, '3.8': 18, '3.9': 19, '4': 20, '4.0': 21, '4.1': 22, '4.2': 23, '4.3': 24, '4.4': 25, '4.5': 26, '4.6': 27, '4.7': 28, '4.8': 29, '4.9': 30, '5': 31, '5.0': 32, '5.1': 33, '5.2': 34, '5.3': 35, '5.4': 36, '5.5': 37, '5.6': 38, '5.7': 39, '5.8': 40, '5.9': 41, '6.0': 42, '6.1': 43, '6.2': 44, '6.3': 45, '6.4': 46, '6.5': 47, '8.0': 48}
            
            pcv_encoded = pcv_map.get(str(int(pcv)), 28) # Default to 28 ('40')
            wc_encoded = wc_map.get(str(int(wc)), 72) # Default to 72 ('7800')
            
            # format rc as decimal string for mapping
            rc_str = f"{rc:.1f}" if int(rc) != rc else str(int(rc))
            rc_encoded = rc_map.get(rc_str, 34) # Default to 34 ('5.2')

            input_data = np.array([[
                age, bp, sg, al, su, rbc_encoded, pc_encoded, pcc_encoded, ba_encoded, bgr, bu, sc, sod, pot, hemo,
                pcv_encoded, wc_encoded, rc_encoded, htn_encoded, dm_encoded, cad_encoded, appet_encoded, pe_encoded, ane_encoded
            ]])
            input_scaled = scalers["kidney"].transform(input_data)
            
            pred_class = models["kidney"].predict(input_scaled)[0]
            prob = models["kidney"].predict_proba(input_scaled)[0]
            
            # Kidney classes: 'ckd':0, 'ckd\t':1, 'notckd':2
            is_ckd = pred_class in [0, 1]
            predicted_result = "High Risk" if is_ckd else "Low Risk"
            risk_score = int((prob[0] + prob[1]) * 100)
            recommendation = get_recommendation("Kidney Disease", 1 if is_ckd else 0)
            pdf_ready = True

    # --------------------------------
    # 5. LIVER DISEASE FORM
    # --------------------------------
    elif disease == "Liver Disease":
        st.subheader("🧪 Hepatobiliary Liver Disease Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=45)
            gender = st.selectbox("Gender", ["Male", "Female"])
            tb = st.number_input("Total Bilirubin (mg/dl)", min_value=0.1, max_value=80.0, value=1.0, step=0.1)
            db = st.number_input("Direct Bilirubin (mg/dl)", min_value=0.1, max_value=20.0, value=0.3, step=0.1)
            ap = st.number_input("Alkaline Phosphotase (IU/L)", min_value=50, max_value=2200, value=150)
        with col2:
            sgpt = st.number_input("Alamine Aminotransferase SGPT (U/L)", min_value=10, max_value=2000, value=35)
            sgot = st.number_input("Aspartate Aminotransferase SGOT (U/L)", min_value=10, max_value=5000, value=35)
            tp = st.number_input("Total Proteins (g/dl)", min_value=2.0, max_value=10.0, value=6.5, step=0.1)
            alb = st.number_input("Albumin (g/dl)", min_value=0.5, max_value=6.0, value=3.5, step=0.1)
            agr = st.number_input("Albumin and Globulin Ratio", min_value=0.1, max_value=3.0, value=1.0, step=0.1)

        if st.button("🔍 Predict Liver Disease Risk"):
            gender_encoded = 1 if gender == "Male" else 0
            
            input_data = np.array([[age, gender_encoded, tb, db, ap, sgpt, sgot, tp, alb, agr]])
            input_scaled = scalers["liver"].transform(input_data)
            
            pred_class = models["liver"].predict(input_scaled)[0]
            prob = models["liver"].predict_proba(input_scaled)[0]
            
            # Liver model outputs: 1 for Liver Disease, 2 for Non-Liver Disease
            is_disease = (pred_class == 1)
            predicted_result = "High Risk" if is_disease else "Low Risk"
            risk_score = int(prob[0] * 100) # Prob of class 1
            recommendation = get_recommendation("Liver Disease", 1 if is_disease else 0)
            pdf_ready = True

    # --------------------------------
    # 6. BREAST CANCER FORM
    # --------------------------------
    elif disease == "Breast Cancer":
        st.subheader("🧴 Breast Cancer Nucleus Feature Analysis")
        st.info("👋 Adjust the cell nuclei measurements below according to the pathology report:")
        
        # Default benign values
        defaults = [13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766, 0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023, 15.11, 19.26, 99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259]
        
        with st.expander("Adjust Nuclei Dimensions (Mean Metrics)", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                r_mean = st.number_input("Radius Mean", value=defaults[0], format="%.5f")
                t_mean = st.number_input("Texture Mean", value=defaults[1], format="%.5f")
                p_mean = st.number_input("Perimeter Mean", value=defaults[2], format="%.5f")
                a_mean = st.number_input("Area Mean", value=defaults[3], format="%.5f")
                s_mean = st.number_input("Smoothness Mean", value=defaults[4], format="%.5f")
            with col2:
                c_mean = st.number_input("Compactness Mean", value=defaults[5], format="%.5f")
                cvy_mean = st.number_input("Concavity Mean", value=defaults[6], format="%.5f")
                cp_mean = st.number_input("Concave Points Mean", value=defaults[7], format="%.5f")
                sym_mean = st.number_input("Symmetry Mean", value=defaults[8], format="%.5f")
                fd_mean = st.number_input("Fractal Dimension Mean", value=defaults[9], format="%.5f")
                
        with st.expander("Adjust Nuclei Dimensions (Standard Error)", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                r_se = st.number_input("Radius SE", value=defaults[10], format="%.5f")
                t_se = st.number_input("Texture SE", value=defaults[11], format="%.5f")
                p_se = st.number_input("Perimeter SE", value=defaults[12], format="%.5f")
                a_se = st.number_input("Area SE", value=defaults[13], format="%.5f")
                s_se = st.number_input("Smoothness SE", value=defaults[14], format="%.5f")
            with col2:
                c_se = st.number_input("Compactness SE", value=defaults[15], format="%.5f")
                cvy_se = st.number_input("Concavity SE", value=defaults[16], format="%.5f")
                cp_se = st.number_input("Concave Points SE", value=defaults[17], format="%.5f")
                sym_se = st.number_input("Symmetry SE", value=defaults[18], format="%.5f")
                fd_se = st.number_input("Fractal Dimension SE", value=defaults[19], format="%.5f")

        with st.expander("Adjust Nuclei Dimensions (Worst/Largest Metrics)", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                r_worst = st.number_input("Radius Worst", value=defaults[20], format="%.5f")
                t_worst = st.number_input("Texture Worst", value=defaults[21], format="%.5f")
                p_worst = st.number_input("Perimeter Worst", value=defaults[22], format="%.5f")
                a_worst = st.number_input("Area Worst", value=defaults[23], format="%.5f")
                s_worst = st.number_input("Smoothness Worst", value=defaults[24], format="%.5f")
            with col2:
                c_worst = st.number_input("Compactness Worst", value=defaults[25], format="%.5f")
                cvy_worst = st.number_input("Concavity Worst", value=defaults[26], format="%.5f")
                cp_worst = st.number_input("Concave Points Worst", value=defaults[27], format="%.5f")
                sym_worst = st.number_input("Symmetry Worst", value=defaults[28], format="%.5f")
                fd_worst = st.number_input("Fractal Dimension Worst", value=defaults[29], format="%.5f")

        if st.button("🔍 Predict Breast Cancer Malignancy"):
            input_data = np.array([[
                r_mean, t_mean, p_mean, a_mean, s_mean, c_mean, cvy_mean, cp_mean, sym_mean, fd_mean,
                r_se, t_se, p_se, a_se, s_se, c_se, cvy_se, cp_se, sym_se, fd_se,
                r_worst, t_worst, p_worst, a_worst, s_worst, c_worst, cvy_worst, cp_worst, sym_worst, fd_worst
            ]])
            input_scaled = scalers["breast"].transform(input_data)
            
            pred_class = models["breast"].predict(input_scaled)[0]
            prob = models["breast"].predict_proba(input_scaled)[0]
            
            # Breast cancer: Benign->0, Malignant->1
            predicted_result = "High Risk" if pred_class == 1 else "Low Risk"
            risk_score = int(prob[1] * 100)
            recommendation = get_recommendation("Breast Cancer", pred_class)
            pdf_ready = True

    # --------------------------------
    # 7. STROKE RISK FORM
    # --------------------------------
    elif disease == "Stroke":
        st.subheader("🧠 Stroke Risk Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=50)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            hypertension = st.selectbox("Hypertension (High Blood Pressure)", ["No", "Yes"])
            heart_disease = st.selectbox("History of Heart Disease", ["No", "Yes"])
            ever_married = st.selectbox("Ever Married", ["Yes", "No"])
        with col2:
            work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt Job", "Children", "Never Worked"])
            residence = st.selectbox("Residence Type", ["Urban", "Rural"])
            avg_glucose = st.number_input("Average Glucose Level (mg/dL)", value=100.0)
            bmi = st.number_input("BMI (Body Mass Index)", value=25.0)
            smoking = st.selectbox("Smoking Status", ["never smoked", "formerly smoked", "smokes", "Unknown / Prefer not to say"])

        if st.button("🔍 Predict Stroke Risk"):
            # Encodings
            gender_map = {"Female": 0, "Male": 1, "Other": 2}
            gender_encoded = gender_map[gender]
            
            ht_encoded = 1 if hypertension == "Yes" else 0
            hd_encoded = 1 if heart_disease == "Yes" else 0
            married_encoded = 1 if ever_married == "Yes" else 0
            
            work_map = {"Govt Job": 0, "Never Worked": 1, "Private": 2, "Self-employed": 3, "Children": 4}
            work_encoded = work_map[work_type]
            
            residence_encoded = 1 if residence == "Urban" else 0
            
            smoke_map = {"Unknown / Prefer not to say": 0, "formerly smoked": 1, "never smoked": 2, "smokes": 3}
            smoke_encoded = smoke_map[smoking]
            
            input_data = np.array([[
                gender_encoded, age, ht_encoded, hd_encoded, married_encoded, 
                work_encoded, residence_encoded, avg_glucose, bmi, smoke_encoded
            ]])
            input_scaled = scalers["stroke"].transform(input_data)
            
            pred_class = models["stroke"].predict(input_scaled)[0]
            prob = models["stroke"].predict_proba(input_scaled)[0]
            
            predicted_result = "High Risk" if pred_class == 1 else "Low Risk"
            risk_score = int(prob[1] * 100)
            recommendation = get_recommendation("Stroke", pred_class)
            pdf_ready = True

    # --------------------------------
    # 8. LUNG CANCER FORM
    # --------------------------------
    elif disease == "Lung Cancer":
        st.subheader("🫁 Lung Cancer Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (Years)", min_value=1, max_value=120, value=60)
            gender = st.selectbox("Gender", ["Male", "Female"])
            smoking = st.selectbox("Smoking Habits", ["No", "Yes"])
            yellow_fingers = st.selectbox("Yellow Fingers", ["No", "Yes"])
            anxiety = st.selectbox("Anxiety Levels", ["No", "Yes"])
            peer_pressure = st.selectbox("Peer Pressure", ["No", "Yes"])
            chronic_disease = st.selectbox("Chronic Disease History", ["No", "Yes"])
            fatigue = st.selectbox("Fatigue or Weakness", ["No", "Yes"])
        
        with col2:
            allergy = st.selectbox("Allergies", ["No", "Yes"])
            wheezing = st.selectbox("Wheezing", ["No", "Yes"])
            alcohol = st.selectbox("Alcohol Consumption", ["No", "Yes"])
            coughing = st.selectbox("Coughing frequently", ["No", "Yes"])
            shortness_breath = st.selectbox("Shortness of breath", ["No", "Yes"])
            swallowing_diff = st.selectbox("Swallowing Difficulty", ["No", "Yes"])
            chest_pain = st.selectbox("Frequent Chest Pain", ["No", "Yes"])

        if st.button("🔍 Predict Lung Cancer Risk"):
            gender_encoded = 1 if gender == "Male" else 0
            
            # Map "No" to 1, "Yes" to 2 for categorical inputs
            map_fn = lambda x: 2 if x == "Yes" else 1
            
            input_data = np.array([[
                gender_encoded, age, map_fn(smoking), map_fn(yellow_fingers), map_fn(anxiety),
                map_fn(peer_pressure), map_fn(chronic_disease), map_fn(fatigue), map_fn(allergy),
                map_fn(wheezing), map_fn(alcohol), map_fn(coughing), map_fn(shortness_breath),
                map_fn(swallowing_diff), map_fn(chest_pain)
            ]])
            input_scaled = scalers["lung"].transform(input_data)
            
            pred_class = models["lung"].predict(input_scaled)[0]
            prob = models["lung"].predict_proba(input_scaled)[0]
            
            predicted_result = "High Risk" if pred_class == 1 else "Low Risk"
            risk_score = int(prob[1] * 100)
            recommendation = get_recommendation("Lung Cancer", pred_class)
            pdf_ready = True

    # ----------------------------
    # DISPLAY PREDICTION RESULT
    # ----------------------------
    if pdf_ready:
        st.markdown("<hr style='border-color: #E2E8F0; margin: 25px 0;'/>", unsafe_allow_html=True)
        
        # Save to database
        save_prediction(
            st.session_state.username,
            disease,
            predicted_result,
            risk_score
        )
        
        # Main output container
        with st.container(border=True):
            st.markdown("<h3 style='background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; margin-bottom: 20px;'>📊 Predictive Analysis Report</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1.5, 2])
            
            with col1:
                if predicted_result == "High Risk":
                    st.markdown("<div class='high-risk-badge'>⚠ HIGH RISK DETECTED</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='low-risk-badge'>✅ LOW RISK / HEALTHY</div>", unsafe_allow_html=True)
                    
                st.metric("📈 Predictive Confidence Score", f"{risk_score}%")
                st.progress(risk_score)
                
            with col2:
                st.markdown("<h4 style='color: #60A5FA; font-weight: 700; margin-top:0;'>📋 Personalized Care Plan</h4>", unsafe_allow_html=True)
                rec_tabs = st.tabs(["🩺 AI Insights", "🥗 Diet Schedule", "🏃 Exercise Plan"])
                
                with rec_tabs[0]:
                    st.markdown("<div class='rec-card'>", unsafe_allow_html=True)
                    st.markdown(f"**Status:** {recommendation['status']}")
                    st.markdown("<hr style='margin:10px 0; border-color:rgba(255,255,255,0.1);'/>", unsafe_allow_html=True)
                    for item in recommendation["clinical_insights"]:
                        st.markdown(f"• {item}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with rec_tabs[1]:
                    st.markdown("<div class='rec-card'>", unsafe_allow_html=True)
                    st.markdown("**Time-to-Time Meal Recommendations:**")
                    st.markdown("<hr style='margin:10px 0; border-color:rgba(255,255,255,0.1);'/>", unsafe_allow_html=True)
                    for time, food in recommendation["diet_plan"].items():
                        st.markdown(f"**{time}**  \n{food}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with rec_tabs[2]:
                    st.markdown("<div class='rec-card'>", unsafe_allow_html=True)
                    st.markdown("**Daily Exercise & Activity Routine:**")
                    st.markdown("<hr style='margin:10px 0; border-color:rgba(255,255,255,0.1);'/>", unsafe_allow_html=True)
                    for time, activity in recommendation["exercise_plan"].items():
                        st.markdown(f"**{time}**  \n{activity}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
            # PDF Report Button
            st.markdown("<hr style='border-color: #E2E8F0; margin: 15px 0;'/>", unsafe_allow_html=True)
            
            pdf_filename = generate_report(
                st.session_state.username,
                disease,
                predicted_result,
                risk_score,
                recommendation
            )
            
            with open(pdf_filename, "rb") as f:
                pdf_bytes = f.read()
                
            st.download_button(
                label="📥 Download Clinical PDF Report",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf"
            )

# ----------------------------
# PREDICTION HISTORY PAGE
# ----------------------------
elif page == "Prediction History":
    st.markdown("""
        <h1 style='background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.2rem; margin-bottom: 5px;'>⏳ Prediction Log & History</h1>
        <p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 25px;'>Review all historical predictive screenings conducted on your account and export reports.</p>
    """, unsafe_allow_html=True)

    history = get_prediction_history(st.session_state.username)

    if not history:
        st.info("No prediction history found. Run a risk analysis to log results.")
    else:
        # Search & Filter
        col1, col2 = st.columns(2)
        with col1:
            filter_disease = st.selectbox(
                "Filter by Disease", 
                ["All"] + list(set([row[0] for row in history]))
            )
        with col2:
            search_query = st.text_input("Search prediction result (e.g. High Risk)")
            
        # Filtering logic
        filtered_history = history
        if filter_disease != "All":
            filtered_history = [row for row in filtered_history if row[0] == filter_disease]
        if search_query:
            filtered_history = [row for row in filtered_history if search_query.lower() in row[1].lower()]
            
        if not filtered_history:
            st.warning("No records matched your filters.")
        else:
            # Styled Column headers
            st.markdown("<hr style='border-color: #E2E8F0; margin: 15px 0;'/>", unsafe_allow_html=True)
            
            header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([2, 1.8, 1.8, 1.5, 1.5])
            with header_col1:
                st.markdown("<b>📅 Date & Time</b>", unsafe_allow_html=True)
            with header_col2:
                st.markdown("<b>🧬 Disease Target</b>", unsafe_allow_html=True)
            with header_col3:
                st.markdown("<b>📊 Prediction</b>", unsafe_allow_html=True)
            with header_col4:
                st.markdown("<b>📈 Risk Score</b>", unsafe_allow_html=True)
            with header_col5:
                st.markdown("<b>📄 Report</b>", unsafe_allow_html=True)
                
            st.markdown("<hr style='border-color: #E2E8F0; margin: 5px 0 15px 0;'/>", unsafe_allow_html=True)
            
            for i, row in enumerate(filtered_history):
                # row structure: (disease, prediction, risk_score, date)
                c_date, c_disease, c_pred, c_score = row[3], row[0], row[1], row[2]
                
                col1, col2, col3, col4, col5 = st.columns([2, 1.8, 1.8, 1.5, 1.5])
                with col1:
                    st.write(c_date)
                with col2:
                    st.write(f"**{c_disease}**")
                with col3:
                    if c_pred == "High Risk":
                        st.markdown(f"<span style='color:#EF4444; font-weight:700;'>⚠ {c_pred}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='color:#10B981; font-weight:700;'>✅ {c_pred}</span>", unsafe_allow_html=True)
                with col4:
                    st.write(f"{c_score}%")
                with col5:
                    # Generate report bytes
                    rec = get_recommendation(c_disease, 1 if c_pred == "High Risk" else 0)
                    pdf_filename = generate_report(
                        st.session_state.username, 
                        c_disease, 
                        c_pred, 
                        c_score, 
                        rec
                    )
                    
                    with open(pdf_filename, "rb") as f:
                        pdf_bytes = f.read()
                        
                    st.download_button(
                        label="📥 PDF",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        key=f"dl_hist_{i}_{c_date.replace(' ', '_').replace(':', '_')}"
                    )
                st.markdown("<hr style='border-color: #F1F5F9; margin: 8px 0;'/>", unsafe_allow_html=True)