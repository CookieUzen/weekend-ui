import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from joblib import load, dump
import time
import copy


# XGB model part
@st.cache_resource
def load_xgb_model():
    loaded_model = xgb.XGBClassifier()
    # loaded_model.load_model('xgb_model.json')
    loaded_model.load_model('xgb_model2.json')
    return loaded_model

def categorize_age(age):

# Define the age categories and their corresponding labels
    age_categories = {
        '0': range(18, 25),
        '1': range(25, 30),
        '2': range(30, 35),
        '3': range(35, 40),
        '4': range(40, 45),
        '5': range(45, 50),
        '6': range(50, 55),
        '7': range(55, 60),
        '8': range(60, 65),
        '9': range(65, 70),
        '10': range(70, 75),
        '11': range(75, 80),
        '12': range(80, 150)  
    }

    # Loop through the dictionary and find the matching age category
    for category, age_range in age_categories.items():
        if age in age_range:
            return category

    return "Unknown"  # Return 'Unknown' if age does not fit any category

def categorize_race(race):

    # Initialize all race category flags as a list of zeros
    races = [0] * 6  # One slot for each race category

    # Only set the appropriate index based on user input
    if 0 <= race < len(races):
        races[race] = 1

    return races

def get_user_input(): 
    #Categorize
    input = copy.copy(st.session_state.user_data)
    
    # Loop through dicationary to turn Yes to No
    for key in input:
        if input[key] == 'Yes':
            input[key] = 1
        elif input[key] == 'No':
            input[key] = 0

    # Parse Biological Sex
    if input['sex'] == 'Female':
        input['sex'] = 0
    else:
        input['sex'] = 1

    # Calculate BMI from height and weight
    try:
        input['BMI'] = input['weight'] / ((input['height'] / 100) ** 2)
    except ZeroDivisionError:
        st.warning("Please enter a non-zero height")
        st.stop()

    # American Indian/Alaskan Native = 0. Asian = 1. Black = 2. White = 3. Hispanic = 4. Other = 5.
    race = input['race']
    if race == 'American Indian/Alaskan Native':
        race = 0
    elif race == 'Asian':
        race = 1
    elif race == 'Black':
        race = 2
    elif race == 'White':
        race = 3
    elif race == 'Hispanic':
        race = 4
    else:
        race = 5
    
    # Store our user data for processing
    input['age'] = categorize_age(input['age'])
    input['races'] = categorize_race(race)

    # TODO: Figure out how to normalize afterwards
    # translated_input['scaler'] = joblib.load('scaler.save')

    if st.session_state.debug:
        st.write(input)

    return np.array([[input['BMI'],
                     input['smoking'],
	                 input['alcohol'],
	                 input['stroke'],
	                 input['diffWalking'],
	                 input['sex'],
	                 input['age'],
	                 # input['diabetic'],
	                 input['physicalActivity'],
	                 input['sleepTime'],
	                 # input['asthma'],
	                 input['kidneyDisease'],
	                 input['skinCancer'],
                     ] + input['races']]
    )

def runInference(model):
    user_input = get_user_input()
    user_input = user_input.astype(np.float32)
    
    if st.session_state.debug:
        st.write(user_input)

    predicted = model.predict(user_input)
    pred_prob = model.predict_proba(user_input)
    return predicted, pred_prob


def train_and_save_sleep_xgb_model(dataset_path):
    dataset = pd.read_csv(dataset_path)
    dataset['Sleep Disorder'].fillna('Normal', inplace=True)

    cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
    
    # Assuming 'BMI' is a numeric column, add it to num_cols if available in your dataset
    num_cols = []  # List numeric columns here, like ['BMI'] if BMI is part of your dataset
    
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        dataset[col] = le.fit_transform(dataset[col])
        label_encoders[col] = le
        dump(le, f'./{col}_label_encoder_xgb.joblib')

    # Scale the numerical features if there are any
    scaler = StandardScaler()
    if num_cols:
        dataset[num_cols] = scaler.fit_transform(dataset[num_cols])
    dump(scaler, './xgb_sleep_scaler.joblib')
    
    features = dataset[cat_cols + num_cols]
    target = dataset['Sleep Disorder']

    model = xgb.XGBClassifier(objective='multi:softmax', num_class=len(set(target)))
    model.fit(features, target)
    
    model.save_model('./xgb_sleep_model.json')

    return model, label_encoders, scaler


@st.cache_resource
def load_xgb_sleep_model():
    try:
        model = load('xgb_sleep_model.joblib')
        scaler = load('xgb_sleep_scaler.joblib')
        label_encoders = {col: load(f'{col}_label_encoder_xgb.joblib') for col in ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']}
    except Exception as e:
        st.error(f"Error loading the XGBoost model for sleep disorders: {e}")
        return None, None, None
    return model, scaler, label_encoders

def predict_sleep_disorders(new_data, model, label_encoders, scaler, label_encoder_y):
    features = []
    for col in label_encoders.keys():
        try:
            # Attempt to transform each feature using the corresponding label encoder
            encoded_feature = label_encoders[col].transform([new_data[col]])[0]
        except ValueError:
            # Handle the case where the label encoder encounters an unseen label
            # Here, we're assigning a default value; you might choose the most common class, etc.
            # For a robust approach, log this issue and handle it according to your application's needs.
            encoded_feature = label_encoders[col].transform([label_encoders[col].classes_[0]])[0]  # Default to first class
        features.append(encoded_feature)
    
    # Scale the features and predict using the model
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)
    decoded_prediction = label_encoder_y.inverse_transform(prediction)  # Decode prediction back to string label
    
    return decoded_prediction


# Sidebar for selecting model type
model_type = st.sidebar.selectbox("Select Model Type", ["Skin Health Prediction", "Sleep Disorder Prediction"])

# Based on selection, either load the health or sleep model
if model_type == "Skin Health Prediction":
    # check data first
    if 'user_data' not in st.session_state:
        st.warning("Please load user skin data in Main Page first!")
        st.stop()

    with st.status("Loading", expanded=True, state="running") as status:
        # Task 1
        progress_text = "Processing Data"
        my_bar = st.progress(50, text=progress_text)
        model_input_array = get_user_input()
        time.sleep(0.3)
        my_bar.progress(100, text=progress_text)

        # Task 2
        progress_text = "Loading model"
        my_bar = st.progress(0, text=progress_text)
        model = load_xgb_model()

        for percent_complete in range(100):
            time.sleep(0.01)
            # increment the progress bar
            my_bar.progress(percent_complete + 1, text=progress_text)

        # Task 3
        progress_text = "Making Predictions"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)

            my_bar.progress(percent_complete + 1, text=progress_text)

        st.session_state.prediction, st.session_state.pred_prob = runInference(model)
        st.session_state.prediction = st.session_state.prediction[0]

        time.sleep(1)
        status.update(label="Done!", state="complete", expanded=False)

    st.header('Prediction Results')

    if st.session_state.debug:
        st.write(st.session_state.prediction)
        st.write(st.session_state.pred_prob)

    issue = False

    # heart disease, diabetic, asthma
    if st.session_state.prediction[0] == 1:
        st.write("You are at risk of developing a heart disease.")
        issue = True

    if st.session_state.prediction[1] == 1:
        st.write("You are at risk of developing diabetes.")
        issue = True

    if st.session_state.prediction[2] == 1:
        st.write("You are at risk of developing asthma.")
        issue = True

    if issue == False:
        st.write("You are not at risk of developing any health issue! 😋")

    
elif model_type == "Sleep Disorder Prediction":
    with st.status("Loading", expanded=True, state="running") as status:
        # Task 1
        progress_text = "Processing Data"
        my_bar = st.progress(50, text=progress_text)
        # check data first
        if 'user_sleep_data' not in st.session_state :
            st.warning("Please load user data in Main Page first!")
            st.stop()
        time.sleep(0.3)
        my_bar.progress(100, text=progress_text)

        # Task 2
        progress_text = "Loading model"
        my_bar = st.progress(0, text=progress_text)

        user_data = st.session_state.user_sleep_data
        
        # Load Logistic Regression model
        # try:
        #     model, scaler, label_encoders = load_xgb_sleep_model()
        #     prediction = predict_sleep_disorders(user_data, label_encoders, scaler, model)
        #     st.write("Your Sleep Disorder Prediction Results:")
        model, label_encoders, scaler, label_encoder_y  = train_and_save_sleep_xgb_model('./Sleep_health_and_lifestyle_dataset.csv')
        

    prediction = predict_sleep_disorders(user_data, model, label_encoders, scaler, label_encoder_y )
    st.write("Your Sleep Disorder Prediction Results:")
    st.write(prediction)




