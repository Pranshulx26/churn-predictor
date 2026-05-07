import streamlit as st 
import requests 
import os 

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

st.set_page_config(page_title='Churn Predictor', page_icon="📡")

st.title('📡 Customer Churn Predictor')
st.markdown('Enter customer details to predict churn risk.')

st.sidebar.header('Customer Profile')

tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)
monthly_charges  = st.sidebar.slider("Monthly Charges ($)", 0.0, 120.0, 65.0)
total_charges    = st.sidebar.number_input("Total Charges ($)", 0.0, 10000.0, 
                                            value=float(tenure * monthly_charges))

senior_citizen   = st.sidebar.selectbox("Senior Citizen", ["No", "Yes"])
partner          = st.sidebar.selectbox("Has Partner", ["No", "Yes"])
dependents       = st.sidebar.selectbox("Has Dependents", ["No", "Yes"])
phone_service    = st.sidebar.selectbox("Phone Service", ["No", "Yes"])
paperless        = st.sidebar.selectbox("Paperless Billing", ["No", "Yes"])
gender           = st.sidebar.selectbox("Gender", ["Female", "Male"])

internet_service = st.sidebar.selectbox("Internet Service", 
                                         ["DSL", "Fiber optic", "No"])
contract         = st.sidebar.selectbox("Contract Type", 
                                         ["Month-to-month", "One year", "Two year"])
payment_method   = st.sidebar.selectbox("Payment Method", 
                                         ["Bank transfer (automatic)", 
                                          "Credit card (automatic)", 
                                          "Electronic check", 
                                          "Mailed check"])

online_security  = st.sidebar.selectbox("Online Security", ["No", "Yes"])
online_backup    = st.sidebar.selectbox("Online Backup",   ["No", "Yes"])
device_protect   = st.sidebar.selectbox("Device Protection", ["No", "Yes"])
tech_support     = st.sidebar.selectbox("Tech Support",    ["No", "Yes"])
streaming_tv     = st.sidebar.selectbox("Streaming TV",    ["No", "Yes"])
streaming_movies = st.sidebar.selectbox("Streaming Movies",["No", "Yes"])
multiple_lines   = st.sidebar.selectbox("Multiple Lines",  ["No", "Yes"])

def yn(val): return 1 if val == "Yes" else 0

payload = {
    "tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "SeniorCitizen": yn(senior_citizen),
    "Partner": yn(partner),
    "Dependents": yn(dependents),
    "PhoneService": yn(phone_service),
    "PaperlessBilling": yn(paperless),
    "gender": 1 if gender == "Male" else 0,
    "MultipleLines_Yes": yn(multiple_lines),
    "InternetService_Fiber_optic": 1 if internet_service == "Fiber optic" else 0,
    "InternetService_No": 1 if internet_service == "No" else 0,
    "OnlineSecurity_Yes": yn(online_security),
    "OnlineBackup_Yes": yn(online_backup),
    "DeviceProtection_Yes": yn(device_protect),
    "TechSupport_Yes": yn(tech_support),
    "StreamingTV_Yes": yn(streaming_tv),
    "StreamingMovies_Yes": yn(streaming_movies),
    "Contract_One_year": 1 if contract == "One year" else 0,
    "Contract_Two_year": 1 if contract == "Two year" else 0,
    "PaymentMethod_Credit_card": 1 if payment_method == "Credit card (automatic)" else 0,
    "PaymentMethod_Electronic_check": 1 if payment_method == "Electronic check" else 0,
    "PaymentMethod_Mailed_check": 1 if payment_method == "Mailed check" else 0,
}


if st.button("Predict Churn Risk", type="primary"):
    with st.spinner("Calling prediction API..."):
        try:
            response = requests.post(API_URL, json=payload)
            result   = response.json()

            prob      = result["churn_probability"]
            risk      = result["risk_level"]
            predicted = result["churn_prediction"]

            # ── Display result ───────────────────────────────────
            st.divider()

            color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[risk]
            st.subheader(f"{color} Risk Level: {risk}")

            st.metric(label="Churn Probability", 
                      value=f"{prob:.1%}")

            st.progress(prob)

            if predicted == 1:
                st.error("⚠️ This customer is likely to churn. "
                         "Consider a retention offer.")
            else:
                st.success("✅ This customer is unlikely to churn.")

            with st.expander("Raw API response"):
                st.json(result)

        except Exception as e:
            st.error(f"API error: {e}. Is the FastAPI server running?")
