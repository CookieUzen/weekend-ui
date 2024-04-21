import streamlit as st
import os

# TODO: DISABLE DEBUG MODE
# if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'false':
#     st.session_state.debug = False
# else:
#     st.session_state.debug = True

st.session_state.debug = False

def collect_user_data():
    '''Pops open a form to collect user data. Updates automatically'''
    user_data = dict()

    with st.form('user_data_form'):
        user_data['sex'] = st.selectbox("Select your biological sex", ('Male', 'Female'))
        user_data['age'] = st.number_input("Enter your age", min_value=18, max_value=100, step=5)
        user_data['race'] = st.selectbox("Enter your race", ('American Indian/Alaskan Native', 'White', 'Black', 'Hispanic', 'Asian', 'Other'))
        user_data['height'] = st.number_input("Enter your height in cm", min_value=1, step=5)
        user_data['weight'] = st.number_input("Enter your weight in kg", min_value=1, step=5)
        user_data['sleepTime'] = st.number_input("Enter sleep time in hours", min_value=0.0, max_value=24.0, step=0.5)
        user_data['physicalActivity'] = st.selectbox("Do you do physical activity?", ('Yes', 'No'), index=0)
        user_data['diabetic'] = st.selectbox("Are you diabetic?", ('Yes', 'No'), index=1)
        user_data['smoking'] = st.selectbox("Do you smoke?", ('Yes', 'No'), index=1)
        user_data['alcohol'] = st.selectbox("Do you drink alcohol?", ('Yes', 'No'), index=1)
        user_data['stroke'] = st.selectbox("Have you had a stroke?", ('Yes', 'No'), index=1)
        user_data['diabetes'] = st.selectbox("Do you have diabetes?", ('Yes', 'No'), index=1)
        user_data['asthma'] = st.selectbox("Do you have asthma?", ('Yes', 'No'), index=1)
        user_data['skinCancer'] = st.selectbox("Do you have skin cancer?", ('Yes', 'No'), index=1)
        user_data['kidneyDisease'] = st.selectbox("Do you have kidney disease?", ('Yes', 'No'), index=1)
        user_data['diffWalking'] = st.selectbox("Do you have difficulty walking?", ('Yes', 'No'), index=1)

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.user_data = user_data

def collect_user_sleep_data():
    '''Collect sleep-specific data from the user.'''
    with st.form('user_sleep_data_form'):
        st.write("Enter your sleep-specific information:")
        user_sleep_data = {}
        user_sleep_data['Age'] = st.number_input("Enter your age", min_value=0, max_value=100, value=25)
        user_sleep_data['Sleep Duration'] = st.number_input("Enter sleep duration in hours", min_value=0.0, max_value=24.0, value=7.0, step=0.1)
        user_sleep_data['Quality of Sleep'] = st.slider("Enter sleep quality score", min_value=1, max_value=10, value=6, step=1)
        user_sleep_data['Daily Steps'] = st.number_input("Enter your daily steps", min_value=0, value=5000)
        user_sleep_data['Gender'] = st.selectbox("Select your gender", ['Male', 'Female'])
        user_sleep_data['BMI Category'] = st.selectbox("Select your BMI Category", ['Normal', 'Overweight', 'Obese', 'Normal weight'])
        user_sleep_data['Blood Pressure'] = '126/83'
        user_sleep_data['Heart Rate'] = st.number_input("Enter your heart rate", min_value=0, max_value=240)
        submitted = st.form_submit_button("Submit Sleep Data")
        if submitted:
            st.session_state.user_sleep_data = user_sleep_data
            st.success("Sleep health data submitted!")

st.set_page_config(
    page_title="Sleep Healthcare & Skin Health App",
    page_icon="🛌",
)
st.header('Sleep Healthcare & Skin Health App')
st.write("Please submit your data in this page to get prediction")

# Load some sample user data
# sample_data = {'Gender':'Male', 'Age': 29, 'Sleep Duration': 6.3, 'BMI Category': 'Normal', 'Blood Pressure': '126/83', 'Heart Rate': 77, 'Daily Steps': 5000}
# if 'user_data' not in st.session_state:
#     st.session_state.user_data = sample_data    

# Sidebar for selecting which form to display
form_choice = st.sidebar.selectbox("Select Form to Fill", ["Skin Health Form", "Sleep Health Form"])

if form_choice == "Skin Health Form":
    collect_user_data()
elif form_choice == "Sleep Health Form":
    collect_user_sleep_data()

# debug
if st.session_state.debug:
    st.write(st.session_state.user_data)
