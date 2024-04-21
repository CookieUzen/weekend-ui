import streamlit as st
import time
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from joblib import load, dump

def predict_new_entry(new_data, label_encoders, scaler, model):
    cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
    for col in cat_cols:
        new_data[col] = label_encoders[col].transform(new_data[col])
    new_data_scaled = scaler.transform(new_data[cat_cols])
    prediction = model.predict(new_data_scaled)
    return prediction

def train_and_save_model(dataset_path):
    dataset = pd.read_csv(dataset_path)
    dataset['Sleep Disorder'].fillna('Normal', inplace=True)

    cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
    label_encoders = {col: LabelEncoder() for col in cat_cols}
    for col in cat_cols:
        dataset[col] = label_encoders[col].fit_transform(dataset[col])
        dump(label_encoders[col], f'{col}_label_encoder.joblib')  # Save each encoder separately

    features = dataset[cat_cols]
    target = dataset['Sleep Disorder']
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    dump(scaler, 'scaler.joblib')

    model = LogisticRegression()
    model.fit(features_scaled, target)
    dump(model, 'model.joblib')
    return model, label_encoders, scaler

# Get our user data from the cache
if 'user_data' not in st.session_state:
    st.warning("Please load user data in Main Page first!")
    st.page_link("./Main_Page.py", label="Click here to go to Main Page")
    st.stop()

user_data = pd.DataFrame.from_dict(st.session_state.user_data, orient='index').T

# Loading status bar
with st.status("Loading", expanded=True, state="running") as status:
    # Task 1
    progress_text = "Loading model"
    my_bar = st.progress(0, text=progress_text)

    try:
        model = load('model.joblib')
        scaler = load('scaler.joblib')
        # Load each label encoder separately
        cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
        label_encoders = {col: load(f'{col}_label_encoder.joblib') for col in cat_cols}
    except Exception as e:
        st.warning(f"Loading failed, error: {str(e)}. Training model...")
        model, label_encoders, scaler = train_and_save_model("./Sleep_health_and_lifestyle_dataset.csv")

    # Replace with model loading function
    for percent_complete in range(100):
        time.sleep(0.01)
        # increment the progress bar
        my_bar.progress(percent_complete + 1, text=progress_text)

    # Delay before bar disappears
    # time.sleep(1)
    # my_bar.empty()

    # Task 2
    progress_text = "Making Predictions"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)

        my_bar.progress(percent_complete + 1, text=progress_text)

    # Prepare and predict
    prediction = predict_new_entry(user_data, label_encoders, scaler, model)
    st.write("Your Health Prediction results:")
    st.write(prediction)


    time.sleep(1)
    status.update(label="Done!", state="complete", expanded=False)

