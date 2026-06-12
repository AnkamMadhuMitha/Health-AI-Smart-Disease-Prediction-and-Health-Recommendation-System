def get_recommendation(disease, prediction):
    # Prediction: 0 for Low Risk, 1 for High Risk
    if prediction == 0:
        return {
            "status": "Low Risk",
            "clinical_insights": [
                "Maintain a healthy, balanced lifestyle and stay active.",
                "Prioritize high-quality sleep (7-8 hours per night) to allow cellular repair.",
                "Ensure proper hydration by drinking at least 2.5 to 3 liters of water daily.",
                "Schedule routine health checkups annually to track vital biomarkers."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Whole grain toast with avocado, two poached eggs, and fresh orange juice.",
                "01:00 PM - Lunch": "Grilled chicken breast or sautéed tofu with quinoa, cucumber salad, and olive oil.",
                "04:30 PM - Evening Snack": "A cup of green tea and a small bowl of Greek yogurt with honey.",
                "08:00 PM - Dinner": "Baked cod or lentil soup, roasted sweet potatoes, asparagus, and a side green salad."
            },
            "exercise_plan": {
                "07:00 AM - Morning Exercise": "30 minutes of aerobic exercise (cycling, brisk walking, or jogging).",
                "06:00 PM - Evening Exercise": "10-15 minutes of full-body dynamic stretching and deep breathing exercises."
            }
        }

    if disease == "Diabetes":
        return {
            "status": "High Risk of Diabetes",
            "clinical_insights": [
                "Limit simple carbohydrates, processed foods, and refined sugars to manage glucose spikes.",
                "Monitor fasting and post-prandial blood glucose levels regularly.",
                "Consult an endocrinologist for a comprehensive metabolic and HbA1c evaluation."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Steel-cut oatmeal topped with raw almonds, chia seeds, and cinnamon (no added sugar).",
                "01:00 PM - Lunch": "Large leafy green salad with grilled salmon or chickpeas, steamed broccoli, and olive oil.",
                "04:30 PM - Evening Snack": "Fresh cucumber and bell pepper slices with two tablespoons of hummus.",
                "08:00 PM - Dinner": "Stir-fried tofu or lean chicken breast with bell peppers, spinach, and cauliflower rice."
            },
            "exercise_plan": {
                "07:00 AM - Morning Exercise": "35 minutes of brisk outdoor walking, cycling, or swimming to improve insulin sensitivity.",
                "08:30 PM - Post-Dinner Walk": "15 minutes of light, slow-paced strolling to help reduce post-meal blood sugar spikes."
            }
        }

    elif disease == "Heart Disease":
        return {
            "status": "High Risk of Heart Disease",
            "clinical_insights": [
                "Strictly limit sodium intake (less than 1,500 mg daily) and avoid trans/saturated fats.",
                "Completely avoid smoking, vaping, and exposure to secondhand smoke.",
                "Regularly monitor blood pressure and cholesterol levels."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "A bowl of oats with blueberries, ground flaxseeds, and a cup of unsweetened hibiscus tea.",
                "01:00 PM - Lunch": "Mediterranean whole-wheat wrap filled with hummus, spinach, sliced tomatoes, and grilled chicken.",
                "04:30 PM - Evening Snack": "Organic apple slices paired with a single tablespoon of natural, unsalted almond butter.",
                "08:00 PM - Dinner": "Grilled mackerel or a rich lentil dahl, roasted Brussels sprouts, and a small side of wild rice."
            },
            "exercise_plan": {
                "07:30 AM - Morning Exercise": "30-40 minutes of moderate cardiovascular workout (steady swimming, brisk walking, or light rowing).",
                "06:00 PM - Evening Exercise": "15 minutes of light restorative yoga focusing on blood circulation and deep relaxation."
            }
        }

    elif disease == "Parkinson's":
        return {
            "status": "Parkinson's Risk Detected",
            "clinical_insights": [
                "Engage in structured gait and balance training to optimize motor stability.",
                "Practice vocal, reading, and speech exercises daily to maintain vocal fold strength.",
                "Schedule a comprehensive neurological checkup with a movement disorder specialist."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Greek yogurt topped with walnuts, blueberries, and a light drizzle of raw organic honey.",
                "01:00 PM - Lunch": "Turkey or tofu sandwich on sprouted grain bread with lettuce, tomatoes, and a cup of vegetable soup.",
                "04:30 PM - Evening Snack": "A cup of green tea and a small piece of dark chocolate (70%+ cacao) rich in antioxidants.",
                "08:00 PM - Dinner": "Baked salmon or stewed kidney beans, mashed sweet potato, and steamed green beans."
            },
            "exercise_plan": {
                "08:00 AM - Morning Exercise": "25 minutes of specialized coordination exercises (e.g. Tai Chi or structured balance walking).",
                "05:00 PM - Evening Exercise": "15 minutes of vocal exercises (reading aloud, exaggerated pronunciation, and humming)."
            }
        }

    elif disease == "Kidney Disease":
        return {
            "status": "Kidney Disease Risk Detected",
            "clinical_insights": [
                "Restrict dietary sodium, potassium, and phosphorus to reduce the kidney filtration load.",
                "Strictly avoid over-the-counter NSAIDs (painkillers) which can accelerate renal damage.",
                "Regularly monitor kidney function markers (eGFR, serum creatinine, and blood urea nitrogen)."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Egg white omelet cooked with bell peppers and onions, served with one slice of sourdough toast.",
                "01:00 PM - Lunch": "Rice noodles with stir-fried chicken breast, cabbage, and carrots (prepared with minimal salt).",
                "04:30 PM - Evening Snack": "A small cup of fresh blueberries, red grapes, or strawberries (low potassium selections).",
                "08:00 PM - Dinner": "Baked cod or sea bass, steamed julienned carrots, and a small portion of white rice."
            },
            "exercise_plan": {
                "07:00 AM - Morning Exercise": "20-30 minutes of low-impact cardiovascular activity (slow walking or stationary cycling).",
                "06:00 PM - Evening Exercise": "10 minutes of gentle, restorative stretching focusing on muscle relaxation and lower back support."
            }
        }

    elif disease == "Liver Disease":
        return {
            "status": "Liver Disease Risk Detected",
            "clinical_insights": [
                "Avoid alcohol consumption entirely to prevent further hepatocyte irritation.",
                "Limit the intake of deep-fried, fatty, and highly processed sugary foods.",
                "Maintain a healthy body mass index (BMI) to reduce the risk of non-alcoholic fatty liver."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Whole-grain porridge cooked in water, topped with fresh strawberries and pumpkin seeds.",
                "01:00 PM - Lunch": "Quinoa bowl loaded with steamed zucchini, carrots, grilled chicken breast, and a drizzle of olive oil.",
                "04:30 PM - Evening Snack": "Celery sticks with a tablespoon of peanut butter, or a fresh pear.",
                "08:00 PM - Dinner": "Steamed white fish, roasted asparagus spears, and a side of brown rice."
            },
            "exercise_plan": {
                "07:00 AM - Morning Exercise": "30 minutes of aerobic exercise (brisk walking, jog, or cross-trainer).",
                "05:30 PM - Evening Exercise": "15 minutes of light resistance training or bodyweight squats to build active lean muscle."
            }
        }

    elif disease == "Breast Cancer":
        return {
            "status": "Breast Cancer Risk Detected",
            "clinical_insights": [
                "Schedule an diagnostic breast ultrasound or mammogram with a specialist.",
                "Perform routine monthly self-examinations to monitor for physical changes.",
                "Emphasize antioxidant-rich diets including cruciferous vegetables."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Green smoothie with spinach, kale, wild blueberries, chia seeds, and unsweetened almond milk.",
                "01:00 PM - Lunch": "Steamed broccoli, Brussels sprouts, and cauliflower served with grilled salmon and quinoa.",
                "04:30 PM - Evening Snack": "Raw carrot and cucumber sticks with a small portion of fresh guacamole.",
                "08:00 PM - Dinner": "Lentil vegetable curry cooked with turmeric, ginger, and garlic, served with a leafy green salad."
            },
            "exercise_plan": {
                "07:30 AM - Morning Exercise": "30 minutes of moderate aerobic training (such as light jogging, walking, or stationary elliptical).",
                "06:00 PM - Evening Exercise": "15 minutes of breathing exercises and mindfulness meditation to help manage cortisol and stress."
            }
        }

    elif disease == "Stroke":
        return {
            "status": "Stroke Risk Detected",
            "clinical_insights": [
                "Keep blood pressure and LDL cholesterol levels tightly controlled.",
                "Incorporate stress-reduction practices (meditation, cognitive therapy) daily.",
                "Maintain daily physical exercise to support arterial health and cerebral blood flow."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Steel-cut oatmeal served with walnuts, ground flaxseeds, and fresh raspberries.",
                "01:00 PM - Lunch": "Spinach salad topped with cherry tomatoes, cucumbers, grilled chicken breast, and light olive oil vinaigrette.",
                "04:30 PM - Evening Snack": "Fresh orange or grapefruit slices rich in Vitamin C.",
                "08:00 PM - Dinner": "Baked trout or plant-based bean patties, steamed asparagus, and wild rice."
            },
            "exercise_plan": {
                "07:00 AM - Morning Exercise": "30-40 minutes of steady cardiovascular training (brisk walking, swimming, or water aerobics).",
                "06:00 PM - Evening Exercise": "15 minutes of breathing exercises and mindfulness to aid vagal tone and lower blood pressure."
            }
        }

    elif disease == "Lung Cancer":
        return {
            "status": "Lung Cancer Risk Detected",
            "clinical_insights": [
                "Avoid smoking, secondhand smoke, and occupational exposure to chemical fumes or dust.",
                "Optimize indoor ventilation and consider using a high-efficiency HEPA air purifier.",
                "Consult a pulmonologist for a clinical lung assessment and potential low-dose CT scan."
            ],
            "diet_plan": {
                "08:00 AM - Breakfast": "Papaya or citrus fruit salad, two soft poached eggs, and a cup of green tea.",
                "01:00 PM - Lunch": "Mixed microgreens with tomatoes, sliced walnuts, grilled chicken, and olive oil dressing.",
                "04:30 PM - Evening Snack": "A small bowl of mixed nuts (focusing on selenium-rich Brazil nuts and almonds).",
                "08:00 PM - Dinner": "Baked salmon, sautéed broccoli, shiitake mushrooms, and roasted sweet potato slices."
            },
            "exercise_plan": {
                "07:00 AM - Morning Exercise": "25-30 minutes of light outdoor walking or swimming to promote lung capacity.",
                "06:00 PM - Evening Exercise": "10-15 minutes of diaphragmatic breathing routines and yoga chest-opening poses."
            }
        }

    return {
        "status": "Recommendation Pending",
        "clinical_insights": ["Consult a medical professional for custom clinical advice."],
        "diet_plan": {"General": "Eat a balanced, low-sodium diet and stay hydrated."},
        "exercise_plan": {"General": "Perform 30 minutes of light exercise daily."}
    }
