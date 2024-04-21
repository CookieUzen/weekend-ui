import streamlit as st
import os

# TODO: DISABLE DEBUG MODE
if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'false':
    st.session_state.debug = False
else:
    st.session_state.debug = True

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

st.set_page_config(
    page_title="Sleep Healthcare & Skin Health App",
    page_icon="🛌",
)
st.header('Sleep Healthcare & Skin Health App')
st.write("Upload and visualize data from the Sleep health and lifestyle dataset.")

# Load some sample user data
# sample_data = {'Gender':'Male', 'Age': 29, 'Sleep Duration': 6.3, 'BMI Category': 'Normal', 'Blood Pressure': '126/83', 'Heart Rate': 77, 'Daily Steps': 5000}
# if 'user_data' not in st.session_state:
#     st.session_state.user_data = sample_data    

collect_user_data()

# debug
if st.session_state.debug:
    st.write(st.session_state.user_data)
