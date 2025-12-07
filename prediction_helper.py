import pandas as pd
import os
from joblib import load

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_rest = load(os.path.join(BASE_DIR, "artifacts", "model_rest.joblib"))
model_young = load(os.path.join(BASE_DIR, "artifacts", "model_young.joblib"))

scaler_rest = load(os.path.join(BASE_DIR, "artifacts", "scaler_rest.joblib"))
scaler_young = load(os.path.join(BASE_DIR, "artifacts", "scaler_young.joblib"))

def calculate_normalized_risk(medical_history):
    # Risk score mapping
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    # Split diseases
    diseases = medical_history.lower().split(" & ")

    # Calculate total raw score
    total_score = 0
    for d in diseases:
        total_score += risk_scores.get(d, 0)  # if unknown disease -> 0

    # Normalization range
    min_score = 0       # minimum possible
    max_score = 6 + 8   # maximum possible = diabetes + heart disease = 14

    # Normalized risk score: (x-min)/(max-min)
    normalized_score = (total_score - min_score) / (max_score - min_score)

    return round(normalized_score, 4)


def preprocess_input(input_dict):
    expected_columns = [
    'age','number_of_dependants','income_lakhs','insurance_plan',
    'genetical_risk','normalized_risk_score','gender_Male','region_Northwest',
    'region_Southeast','region_Southwest','marital_status_Unmarried',
    'bmi_category_Obesity','bmi_category_Overweight','bmi_category_Underweight',
    'smoking_status_Occasional','smoking_status_Regular','employment_status_Salaried',
    'employment_status_Self-Employed'
    ]

    insurance_plan_encoding = {'Bronze':1,'Silver':2,'Gold':3}
    df = pd.DataFrame(0,columns=expected_columns, index=[0])

    df.loc[0, "age"] = input_dict.get("age", 0)
    df.loc[0, "number_of_dependants"] = input_dict.get("number_of_dependants", 0)
    df.loc[0, "income_lakhs"] = input_dict.get("income_lakhs", 0)

    # ---------- Insurance Plan Value ----------
    if input_dict["insurance_plan"] in insurance_plan_encoding:
        df.loc[0, "insurance_plan"] = insurance_plan_encoding[input_dict["insurance_plan"]]

    # ---------- Gender ----------
    if input_dict["gender"] == "Male":
        df.loc[0, "gender_Male"] = 1

    # ---------- Region ----------
    if input_dict["region"] == "Northwest":
        df.loc[0, "region_Northwest"] = 1
    elif input_dict["region"] == "Southeast":
        df.loc[0, "region_Southeast"] = 1
    elif input_dict["region"] == "Southwest":
        df.loc[0, "region_Southwest"] = 1
    # Northeast remains all zeros (base class)

    # ---------- Marital Status ----------
    if input_dict["marital_status"] == "Unmarried":
        df.loc[0, "marital_status_Unmarried"] = 1

    # ---------- BMI Category ----------
    if input_dict["bmi_category"] == "Obesity":
        df.loc[0, "bmi_category_Obesity"] = 1
    elif input_dict["bmi_category"] == "Overweight":
        df.loc[0, "bmi_category_Overweight"] = 1
    elif input_dict["bmi_category"] == "Underweight":
        df.loc[0, "bmi_category_Underweight"] = 1
    # Normal remains base=0

    # ---------- Smoking ----------
    if input_dict["smoking_status"] == "Occasional":
        df.loc[0, "smoking_status_Occasional"] = 1
    elif input_dict["smoking_status"] == "Regular":
        df.loc[0, "smoking_status_Regular"] = 1
    # No Smoking = base=0

    # ---------- Employment Status ----------
    if input_dict["employment_status"] == "Salaried":
        df.loc[0, "employment_status_Salaried"] = 1
    elif input_dict["employment_status"] == "Self-Employed":
        df.loc[0, "employment_status_Self-Employed"] = 1

    df['normalized_risk_score'] = calculate_normalized_risk(input_dict['medical_history'])
    df = handle_scaling(input_dict['age'], df)
    return df

def handle_scaling(age, df):
    if age>=25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    col_scale = scaler_object['col_scale']
    scaler = scaler_object['scaler']

    df['income_level'] = None
    df[col_scale] = scaler.transform(df[col_scale])
    df.drop('income_level', axis='columns', inplace=True)
    return df

def predict(input_dict):
    input_df = preprocess_input(input_dict)

    if input_dict['age'] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return prediction
