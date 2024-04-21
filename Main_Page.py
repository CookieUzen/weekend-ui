import streamlit as st
import os
import copy

# TODO: DISABLE DEBUG MODE
if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'false':
    st.session_state.debug = False
else:
    st.session_state.debug = True

def collect_user_data():
    '''Pops open a form to collect user data. Updates automatically'''
    user_data = copy.copy(st.session_state.user_data)

    with st.form('user_data_form'):
        user_data['Age'] = st.number_input("Enter your age", min_value=0, max_value=100, value=user_data['Age'])
        user_data['Sleep Duration'] = st.number_input("Enter sleep duration in hours", min_value=0.0, max_value=24.0, value=user_data['Sleep Duration'], step=0.1)
        user_data['Quality of Sleep'] = st.slider("Enter sleep quality score", min_value=1, max_value=10, value=user_data['Quality of Sleep'], step=1)
        user_data['Sleep Disorder'] = st.multiselect("Select any sleep disorders you have", ['Insomnia', 'Sleep Apnea', 'Narcolepsy', 'None'], default=user_data['Sleep Disorder'])

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.user_data = user_data


st.set_page_config(
    page_title="Sleep Healthcare App",
    page_icon="🛌",
)
st.header('Sleep Healthcare App')
st.write("Upload and visualize data from the Sleep health and lifestyle dataset.")

# Load some sample user data
sample_data = {'Age': 25, 'Sleep Duration': 7.0, 'Quality of Sleep': 6, 'BMI': 'Normal', 'Sleep Disorder': [], 'Occupation':'Software Engineer', 'Stress Level': 4 }
if 'user_data' not in st.session_state:
    st.session_state.user_data = sample_data    

collect_user_data()

# debug
if st.session_state.debug:
    st.write(st.session_state.user_data)
