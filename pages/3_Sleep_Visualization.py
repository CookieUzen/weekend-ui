import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

def plot_age_vs_sleep_quality(data, input_user_data=None):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Age', y='Quality of Sleep', data=data, color='blue', alpha=0.6)
    if input_user_data is not None:
        sns.scatterplot(x='Age', y='Quality of Sleep', data=input_user_data, color='red', marker='o', s=100)
    plt.title('Relationship Between Age and Quality of Sleep')
    plt.xlabel('Age (years)')
    plt.ylabel('Quality of Sleep')
    plt.grid(True)
    st.pyplot(plt)

def plot_sleep_duration_vs_quality(data, input_user_data=None):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Sleep Duration', y='Quality of Sleep', data=data, color='blue')
    if input_user_data is not None:
        sns.scatterplot(x='Sleep Duration', y='Quality of Sleep', data=input_user_data, color='red', marker='o', s=100)
    plt.title('Relationship Between Sleep Duration and Quality of Sleep')
    plt.xlabel('Sleep Duration (hours)')
    plt.ylabel('Quality of Sleep')
    st.pyplot(plt)

def plot_occupation_vs_sleep_quality(data):
    plt.figure(figsize=(10, 6))
    occupation_sleep_quality = data.groupby('Occupation')['Quality of Sleep'].mean().sort_values()
    sns.barplot(x=occupation_sleep_quality.values, y=occupation_sleep_quality.index, orient='h')
    plt.title('Average Sleep Quality by Occupation')
    plt.xlabel('Average Quality of Sleep')
    plt.ylabel('Occupation')
    st.pyplot(plt)

def plot_bmi_vs_heart_rate(data):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='BMI Category', y='Heart Rate', data=data)
    plt.title('Heart Rate Distribution by BMI Category')
    plt.xlabel('BMI Category')
    plt.ylabel('Heart Rate')
    st.pyplot(plt)

def plot_stress_vs_sleep_disorders(data):
    plt.figure(figsize=(10, 6))
    stress_sleep_disorder = data.groupby('Stress Level')['Sleep Disorder'].value_counts().unstack().fillna(0)
    stress_sleep_disorder.plot(kind='bar', stacked=True)
    plt.title('Sleep Disorders Distribution by Stress Level')
    plt.xlabel('Stress Level')
    plt.ylabel('Count')
    st.pyplot(plt)

# 使用st.cache装饰器来缓存加载的数据
@st.cache_resource
def load_data(uploaded_file='./Sleep_health_and_lifestyle_dataset.csv'):
    # 读取CSV文件内容为Pandas DataFrame
    with st.status("Loading internal database", expanded=False, state="running") as status_bar:
        data = pd.read_csv(uploaded_file)
        time.sleep(0.5)
    return data

# 显示DataFrame的内容
st.write("# Average Sleep health data:")
st.write("You can compare your health data with the average value in the chosen chart")

# Get our user data from the cache
if 'user_sleep_data' not in st.session_state:
    st.warning("Please load user data in Main Page first!")
    st.page_link("./Main_Page.py", label="Click here to go to Main Page")
    st.stop()

user_sleep_data = pd.DataFrame.from_dict(st.session_state.user_sleep_data, orient='index').T
if st.session_state.debug:
    st.write(st.session_state.user_sleep_data)
    st.write(user_sleep_data)

data = load_data()

# 显示图表选择器
with st.sidebar:
    selected_chart = st.radio(
        "Choose a chart to display",
        options=["Age Distribution", "Sleep Duration vs Quality", "Occupation vs Sleep Quality", 
                "BMI Category vs Heart Rate", "Stress Level vs Sleep Disorders"]
    )

if selected_chart == "Age Distribution":
    plot_age_vs_sleep_quality(data, user_sleep_data)
elif selected_chart == "Sleep Duration vs Quality":
    plot_sleep_duration_vs_quality(data, user_sleep_data)
elif selected_chart == "Occupation vs Sleep Quality":
    plot_occupation_vs_sleep_quality(data)
elif selected_chart == "BMI Category vs Heart Rate":
    plot_bmi_vs_heart_rate(data)
elif selected_chart == "Stress Level vs Sleep Disorders":
    plot_stress_vs_sleep_disorders(data)
