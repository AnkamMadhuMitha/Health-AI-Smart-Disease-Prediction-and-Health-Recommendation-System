from fpdf import FPDF
from datetime import datetime

def sanitize_text(text):
    if not isinstance(text, str):
        return str(text)
    
    # Replace common Unicode symbols and emojis with Latin-1 equivalents
    replacements = {
        "✅": "[OK] ",
        "⚠": "[WARNING] ",
        "•": "- ",
        "—": "-",
        "…": "...",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
        
    # Encode to Latin-1, ignoring unsupported characters to prevent UnicodeEncodeError
    return text.encode("latin-1", "ignore").decode("latin-1")

def generate_report(
    username,
    disease,
    prediction,
    risk_score,
    recommendation
):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # 1. Header Banner Background (Deep Slate Blue)
    pdf.set_fill_color(15, 23, 42) # #0F172A
    pdf.rect(0, 0, 210, 38, "F")
    
    # Header Title
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 20)
    pdf.text(15, 22, sanitize_text("HEALTH AI - CLINICAL REPORT"))
    
    # Header Subtitle
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(148, 163, 184) # Slate grey
    pdf.text(15, 30, sanitize_text("Smart Disease Prediction and Health Recommendation System"))

    # 2. Patient & Diagnostic Info
    pdf.set_y(45)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(30, 41, 59) # Dark Slate
    pdf.cell(190, 8, sanitize_text("PATIENT & DIAGNOSTIC SUMMARY"), ln=True)
    
    # Horizontal line
    pdf.set_draw_color(226, 232, 240) # Slate border
    pdf.line(10, 53, 200, 53)
    pdf.ln(4)
    
    # Patient Data Table
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(95, 7, sanitize_text(f"Patient Name: {username.capitalize()}"), ln=False)
    pdf.cell(95, 7, sanitize_text(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)
    pdf.cell(95, 7, sanitize_text(f"Target Screening: {disease}"), ln=False)
    
    # Dynamic Risk color and confidence
    if prediction == "High Risk":
        pdf.set_text_color(239, 68, 68) # Red
        pdf.set_font("Arial", "B", 10)
        pdf.cell(95, 7, sanitize_text(f"Risk Assessment: HIGH RISK ({risk_score}% Confidence)"), ln=True)
    else:
        pdf.set_text_color(16, 185, 129) # Green
        pdf.set_font("Arial", "B", 10)
        pdf.cell(95, 7, sanitize_text(f"Risk Assessment: LOW RISK / HEALTHY ({risk_score}% Confidence)"), ln=True)

    pdf.ln(8)

    # Parse recommendation structure
    if isinstance(recommendation, dict):
        insights = recommendation.get("clinical_insights", [])
        diet_plan = recommendation.get("diet_plan", {})
        exercise_plan = recommendation.get("exercise_plan", {})
    else:
        insights = [recommendation]
        diet_plan = {}
        exercise_plan = {}

    # 3. Clinical Insights
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 8, sanitize_text("1. AI CLINICAL INSIGHTS"), ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(51, 65, 85)
    for item in insights:
        pdf.multi_cell(0, 6, sanitize_text(f"- {item}"))
    pdf.ln(6)

    # 4. Diet Plan Section (Time-to-Time Table)
    if diet_plan:
        pdf.set_text_color(30, 41, 59)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 8, sanitize_text("2. PERSONALIZED DIET PLAN (TIME-TO-TIME)"), ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        for time, food in diet_plan.items():
            # Time column (Teal style)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(13, 148, 136) # Teal
            pdf.cell(50, 6, sanitize_text(time), ln=False)
            
            # Food column
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 6, sanitize_text(food))
        pdf.ln(6)

    # 5. Exercise Section
    if exercise_plan:
        pdf.set_text_color(30, 41, 59)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 8, sanitize_text("3. PERSONALIZED EXERCISE SCHEDULE"), ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        for time, activity in exercise_plan.items():
            # Time column (Blue style)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(59, 130, 246) # Blue
            pdf.cell(50, 6, sanitize_text(time), ln=False)
            
            # Activity column
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 6, sanitize_text(activity))
        pdf.ln(10)

    # 6. Bottom Disclaimer Section
    pdf.set_y(-25)
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.multi_cell(0, 4, sanitize_text("Disclaimer: This report is generated by Health AI's predictive model for informational screening. It does not replace professional medical advice, diagnosis, or treatment. Please consult a qualified healthcare provider."), align="C")

    # Save to file
    safe_username = "".join(c for c in sanitize_text(username) if c.isalnum() or c in ("-", "_"))
    filename = f"report_{safe_username}.pdf"
    pdf.output(filename)
    return filename
