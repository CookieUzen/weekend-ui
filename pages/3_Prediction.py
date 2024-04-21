import streamlit as st
import time
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb
import pandas as pd
import numpy as np
from joblib import load, dump
import joblib
import copy

def predict_new_entry(new_data, label_encoders, scaler, model):
    cat_cols = ['Gender', 'Age', 'Sleep Duration', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps']
    for col in cat_cols:
        new_data[col] = label_encoders[col].transform(new_data[col])
    new_data_scaled = scaler.transform(new_data[cat_cols])
    prediction = model.predict(new_data_scaled)
    return prediction

@st.cache_resource
def load_model():
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


# Get our user data from the cache
if 'user_data' not in st.session_state:
    st.warning("Please load user data in Main Page first!")
    st.page_link("./Main_Page.py", label="Click here to go to Main Page")
    st.stop()

user_data = pd.DataFrame.from_dict(st.session_state.user_data, orient='index').T

# Loading status bar
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
    model = load_model()

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
