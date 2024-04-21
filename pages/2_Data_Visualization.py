import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")


def plot_bmi_vs_heart_disease(data):
    plt.figure(figsize=(10, 6))
    data['BMI Category'] = pd.cut(data['BMI'], bins=[0, 18.5, 25, 30, 35, 40, 100],
                                  labels=['Underweight', 'Normal weight', 'Overweight', 
                                          'Obesity I', 'Obesity II', 'Obesity III'])
    bmi_heart_disease = data.groupby('BMI Category')['HeartDisease'].mean() * 100
    sns.barplot(x=bmi_heart_disease.index, y=bmi_heart_disease.values, palette='coolwarm')
    plt.title('Heart Disease Prevalence by BMI Category')
    plt.xlabel('BMI Category')
    plt.ylabel('Percentage with Heart Disease (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

def plot_smoking_vs_heart_disease(data):
    plt.figure(figsize=(10, 6))
    smoking_heart_disease = data.groupby('Smoking')['HeartDisease'].mean() * 100
    sns.barplot(x=smoking_heart_disease.index, y=smoking_heart_disease.values, palette='coolwarm')
    plt.title('Heart Disease Prevalence by Smoking Status')
    plt.xlabel('Smoking Status')
    plt.ylabel('Percentage with Heart Disease (%)')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

def plot_age_vs_heart_disease(data):
    plt.figure(figsize=(12, 8))
    age_heart_disease = data.groupby('AgeCategory')['HeartDisease'].mean() * 100
    sns.barplot(x=age_heart_disease.index, y=age_heart_disease.values, palette='viridis')
    plt.title('Heart Disease Prevalence by Age Category')
    plt.xlabel('Age Category')
    plt.ylabel('Percentage with Heart Disease (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

@st.experimental_memo
def load_data(uploaded_file='heart_2020_cleaned.csv'):
    with st.spinner('Loading data...'):
        data = pd.read_csv(uploaded_file)
        data['HeartDisease'] = data['HeartDisease'].map({'Yes': 1, 'No': 0})  # Ensure this conversion early
        time.sleep(0.5)  # Simulate delay for user feedback
    return data

data = load_data()

st.write("# Heart Health Data Overview")
st.write("Below you can compare your health data with the average values in the selected charts.")
st.write("Click at the right sidebar to switch the graph showing on the page")

# Load user data and handle missing data case
user_data = st.session_state.get('user_data', None)
if user_data is None:
    st.warning("Please load user data on the main page first.")
    st.stop()

if st.session_state.get('debug', False):
    st.write(st.session_state.user_data)
    st.write(user_data)

# Chart selection sidebar
with st.sidebar:
    chart_option = st.radio(
        "Choose a chart to display",
        ("BMI vs Heart Disease", "Smoking vs Heart Disease", "Age vs Heart Disease")
    )

if chart_option == "BMI vs Heart Disease":
    plot_bmi_vs_heart_disease(data)
elif chart_option == "Smoking vs Heart Disease":
    plot_smoking_vs_heart_disease(data)
elif chart_option == "Age vs Heart Disease":
    plot_age_vs_heart_disease(data)
