import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from joblib import load, dump
import time

# Function to train and save the Logistic Regression model for sleep disorder predictions
def train_and_save_sleep_model(dataset_path):
    dataset = pd.read_csv(dataset_path)
    dataset['Sleep Disorder'].fillna('Normal', inplace=True)
    cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
    label_encoders = {col: LabelEncoder() for col in cat_cols}
    for col in cat_cols:
        dataset[col] = label_encoders[col].fit_transform(dataset[col])
        dump(label_encoders[col], f'{col}_label_encoder.joblib')

    features = dataset[cat_cols]
    target = dataset['Sleep Disorder']
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    dump(scaler, 'sleep_scaler.joblib')

    model = LogisticRegression()
    model.fit(features_scaled, target)
    dump(model, 'sleep_model.joblib')
    return model, label_encoders, scaler

# Function to predict using the trained model
def predict_new_entry(new_data, label_encoders, scaler, model):
    cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
    for col in cat_cols:
        new_data[col] = label_encoders[col].transform(new_data[col])
    new_data_scaled = scaler.transform(new_data[cat_cols])
    prediction = model.predict(new_data_scaled)
    return prediction

# Load XGBoost model
@st.cache_resource
def load_xgb_model():
    model = xgb.XGBClassifier()
    model.load_model('xgb_model2.json')
    return model

# Sidebar for selecting model type
model_type = st.sidebar.selectbox("Select Model Type", ["Health Prediction", "Sleep Disorder Prediction"])

# Based on selection, either load the health or sleep model
if model_type == "Health Prediction":
    model = load_xgb_model()
    prediction_text = "Your Health Prediction Results:"
elif model_type == "Sleep Disorder Prediction":
    # Load Logistic Regression model
    try:
        model = load('sleep_model.joblib')
        scaler = load('sleep_scaler.joblib')
        cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
        label_encoders = {col: load(f'{col}_label_encoder.joblib') for col in cat_cols}
    except Exception as e:
        st.warning(f"Loading failed, error: {str(e)}. Training model...")
        model, label_encoders, scaler = train_and_save_sleep_model("/mnt/data/Sleep_health_and_lifestyle_dataset.csv")
    prediction_text = "Your Sleep Disorder Prediction Results:"

if 'user_data' not in st.session_state & model_type == "Health Prediction":
    st.warning("Please load user skin data in Main Page first!")
    st.stop()

if 'user_data' not in st.session_state & model_type == "Health Prediction":
    st.warning("Please load user data in Main Page first!")
    st.stop()

user_data = pd.DataFrame.from_dict(st.session_state.user_data, orient='index').T
prediction = predict_new_entry(user_data, label_encoders, scaler, model)

st.header(prediction_text)
st.write(prediction)
