# Customer Churn Predictor

End-to-end ML system that predicts telecom customer churn probability.

**Live demo:** https://churn-predictor-j078.onrender.com

## Stack
- Model: Logistic Regression (ROC-AUC: 0.836)
- Backend: FastAPI + Pydantic
- Frontend: Streamlit
- Deployment: Docker + Render

## Run locally
pip install -r requirements.txt
uvicorn src.api.main:app --reload        # terminal 1

streamlit run src/frontend/app.py        # terminal 2