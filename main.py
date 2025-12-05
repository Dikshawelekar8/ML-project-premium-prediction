import streamlit as st
from prediction_helper import predict

# ------------------ Centered Small Title ------------------
st.markdown("""
    <h3 style='text-align: center; color: black;'>
       🏥 Health Insurance Cost Prediction 🏥 
    </h3>
""", unsafe_allow_html=True)

# ------------------ Centered Subtitle ------------------
st.markdown("""
    <p style='text-align: center; color: black; font-size: 16px;'>
        Fill in the information below to estimate your health insurance cost.
    </p>
""", unsafe_allow_html=True)


# ------------------ Form ------------------
with st.form("insurance_form"):

    # ---- Row 1 ----
    r1c1, r1c2, r1c3 = st.columns(3)
    age = r1c1.number_input("Age", min_value=18, max_value=100, step=1)
    gender = r1c2.selectbox("Gender", ['Male', 'Female'])
    region = r1c3.selectbox("Region", ['Northeast', 'Northwest', 'Southeast', 'Southwest'])

    # ---- Row 2 ----
    r2c1, r2c2, r2c3 = st.columns(3)
    marital_status = r2c1.selectbox("Marital Status", ['Unmarried', 'Married'])
    dependants = r2c2.number_input("Number Of Dependants", min_value=0, max_value=5, value=0)
    bmi_category = r2c3.selectbox("BMI Category", ['Normal','Overweight', 'Underweight','Obesity'])

    # ---- Row 3 ----
    r3c1, r3c2, r3c3 = st.columns(3)
    smoking_status = r3c1.selectbox("Smoking Status",
                                    ['No Smoking', 'Occasional','Regular'])
    employment_status = r3c2.selectbox("Employment Status", ['Self-Employed', 'Freelancer', 'Salaried'])
    genetical_risk = r3c3.number_input("Genetical Risk", min_value=0, value=0)

    # ---- Row 4 ----
    r4c1, r4c2, r4c3 = st.columns(3)
    income_lakhs = r4c1.number_input("Annual Income (Lakhs)", min_value=0, value=0)
    medical_history = r4c2.selectbox("Medical History",
                                     ['No Disease','High blood pressure','Diabetes & High blood pressure',
                                      'Diabetes & Heart disease', 'Diabetes', 'Diabetes & Thyroid',
                                      'Heart disease', 'Thyroid', 'High blood pressure & Heart disease'])
    insurance_plan = r4c3.selectbox("Insurance Plan", ['Silver', 'Bronze', 'Gold'])

    # ---- Collect Input ----
    input_dict = {
        "age": age,
        "gender": gender,
        "region": region,
        "marital_status": marital_status,
        "number_of_dependants": dependants,
        "bmi_category": bmi_category,
        "smoking_status": smoking_status,
        "employment_status": employment_status,
        "genetical_risk_score": genetical_risk,
        "income_lakhs": income_lakhs,
        "medical_history": medical_history,
        "insurance_plan": insurance_plan
    }

    # ---- Predict Button ----
    submit = st.form_submit_button("Predict")

# ---- Prediction Action ----
if submit:
    result = predict(input_dict)
    st.success(f"Estimated Insurance Cost: ₹ {float(result):.2f}")

