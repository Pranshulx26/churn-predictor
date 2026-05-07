from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# Load model, scaler, and exact feature names at startup
model         = joblib.load("src/models/logistic_regression.pkl")
scaler        = joblib.load("src/models/scaler.pkl")
feature_names = joblib.load("src/models/feature_names.pkl")

app = FastAPI(title="Churn Predictor API", version="1.0")


class CustomerFeatures(BaseModel):
    tenure: float
    MonthlyCharges: float
    TotalCharges: float
    SeniorCitizen: int
    Partner: int
    Dependents: int
    PhoneService: int
    PaperlessBilling: int
    gender: int
    MultipleLines_Yes: int
    InternetService_Fiber_optic: int
    InternetService_No: int
    OnlineSecurity_Yes: int
    OnlineBackup_Yes: int
    DeviceProtection_Yes: int
    TechSupport_Yes: int
    StreamingTV_Yes: int
    StreamingMovies_Yes: int
    Contract_One_year: int
    Contract_Two_year: int
    PaymentMethod_Credit_card: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int


# Explicit mapping: Pydantic field name → exact trained column name
FIELD_TO_COLUMN = {
    "tenure": "tenure",
    "MonthlyCharges": "MonthlyCharges",
    "TotalCharges": "TotalCharges",
    "SeniorCitizen": "SeniorCitizen",
    "Partner": "Partner",
    "Dependents": "Dependents",
    "PhoneService": "PhoneService",
    "PaperlessBilling": "PaperlessBilling",
    "gender": "gender",
    "MultipleLines_Yes": "MultipleLines_Yes",
    "InternetService_Fiber_optic": "InternetService_Fiber optic",
    "InternetService_No": "InternetService_No",
    "OnlineSecurity_Yes": "OnlineSecurity_Yes",
    "OnlineBackup_Yes": "OnlineBackup_Yes",
    "DeviceProtection_Yes": "DeviceProtection_Yes",
    "TechSupport_Yes": "TechSupport_Yes",
    "StreamingTV_Yes": "StreamingTV_Yes",
    "StreamingMovies_Yes": "StreamingMovies_Yes",
    "Contract_One_year": "Contract_One year",
    "Contract_Two_year": "Contract_Two year",
    "PaymentMethod_Credit_card": "PaymentMethod_Credit card (automatic)",
    "PaymentMethod_Electronic_check": "PaymentMethod_Electronic check",
    "PaymentMethod_Mailed_check": "PaymentMethod_Mailed check",
}


@app.get("/")
def root():
    return {"message": "Churn Predictor API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: CustomerFeatures):
    # Map Pydantic fields → exact trained column names
    raw = customer.model_dump()
    mapped = {FIELD_TO_COLUMN[k]: v for k, v in raw.items()}

    # Build dataframe with ALL feature columns in correct order
    # Missing columns (unseen categories) default to 0
    input_df = pd.DataFrame([mapped], columns=feature_names).fillna(0)

    # Scale numerical columns
    scale_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    input_df[scale_cols] = scaler.transform(input_df[scale_cols])

    # Predict
    churn_prob = model.predict_proba(input_df)[0][1]
    churn_pred = int(churn_prob >= 0.5)

    return {
        "churn_probability": round(float(churn_prob), 4),
        "churn_prediction": churn_pred,
        "risk_level": "High"   if churn_prob >= 0.7 else
                      "Medium" if churn_prob >= 0.4 else "Low"
    }