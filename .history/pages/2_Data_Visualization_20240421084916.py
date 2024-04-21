import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

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
    plt.show()

def plot_smoking_vs_heart_disease(data):
    plt.figure(figsize=(10, 6))
    smoking_heart_disease = data.groupby('Smoking')['HeartDisease'].mean() * 100
    sns.barplot(x=smoking_heart_disease.index, y=smoking_heart_disease.values, palette='coolwarm')
    plt.title('Heart Disease Prevalence by Smoking Status')
    plt.xlabel('Smoking Status')
    plt.ylabel('Percentage with Heart Disease (%)')
    plt.grid(True)
    plt.show()

def plot_age_vs_heart_disease(data):
    plt.figure(figsize=(12, 8))
    age_heart_disease = data.groupby('AgeCategory')['HeartDisease'].mean() * 100
    sns.barplot(x=age_heart_disease.index, y=age_heart_disease.values, palette='viridis')
    plt.title('Heart Disease Prevalence by Age Category')
    plt.xlabel('Age Category')
    plt.ylabel('Percentage with Heart Disease (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()


# 使用st.cache装饰器来缓存加载的数据
@st.cache_resource
def load_data(uploaded_file='./heart_2020_cleaned.csv'):
    # 读取CSV文件内容为Pandas DataFrame
    with st.status("Loading internal database", expanded=False, state="running") as status_bar:
        data = pd.read_csv(uploaded_file)
        time.sleep(0.5)
        status_bar.update(label="Database loaded!", state="complete", expanded=False)
    return data

# 显示DataFrame的内容
st.write("# Average Sleep health data:")
st.write("You can compare your health data with the average value in the chosen chart")

# Get our user data from the cache
if 'user_data' not in st.session_state:
    st.warning("Please load user data in Main Page first!")
    st.page_link("./Main_Page.py", label="Click here to go to Main Page")
    st.stop()

user_data = pd.DataFrame.from_dict(st.session_state.user_data, orient='index').T
if st.session_state.debug:
    st.write(st.session_state.user_data)
    st.write(user_data)

data = load_data()

# 显示图表选择器
with st.sidebar:
    # Plot selection sidebar
    chart_option = st.sidebar.selectbox(
        "Choose a chart to display",
        ("BMI vs Heart Disease", "Smoking vs Heart Disease", "Age vs Heart Disease")
    )

if chart_option == "BMI vs Heart Disease":
    plot_bmi_vs_heart_disease(data)
elif chart_option == "Smoking vs Heart Disease":
    plot_smoking_vs_heart_disease(data)
elif chart_option == "Age vs Heart Disease":
    plot_age_vs_heart_disease(data)
