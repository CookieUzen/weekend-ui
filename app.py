import streamlit as st
import pandas as pd
import streamlit_option_menu
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# 使用st.cache装饰器来缓存加载的数据
@st.cache
def load_data(uploaded_file):
    # 读取CSV文件内容为Pandas DataFrame
    return pd.read_csv(uploaded_file)

# 创建侧边栏菜单
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Data Visualization", "Disease Prediction"],
        icons=["house", "bar-chart-line", "activity-heartbeat"],
        menu_icon="cast",
        default_index=0,
    )


def collect_user_data():
    with st.form("user_data_form"):
        age = st.number_input("Enter your age", min_value=18, max_value=100, value=30)
        sleep_duration = st.number_input("Enter sleep duration in hours", min_value=0.0, max_value=24.0, value=8.0, step=0.1)
        sleep_quality = st.number_input("Enter sleep quality score", min_value=1, max_value=10, value=5)
        submitted = st.form_submit_button("Submit")
        if submitted:
            return pd.DataFrame({'Age': [age], 'Sleep Duration': [sleep_duration], 'Quality of Sleep': [sleep_quality]})
    return None

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



def main():
    # 根据选中的菜单项展示不同的内容
    if selected == "Home":
        st.title(f"You Have Selected {selected}")
        st.header('Sleep Healthcare App')
        # 假设提到的CSV文件是示例数据文件，下面这行可以显示文件的一些信息或者内容
        st.write("Upload and visualize data from the Sleep health and lifestyle dataset.")

    elif selected == "Data Visualization":
        # # 创建一个文件上传器让用户上传CSV文件
        # uploaded_file = st.file_uploader("Choose a CSV file to upload", type="csv")
        uploaded_file = "./Sleep_health_and_lifestyle_dataset.csv"

        # 显示DataFrame的内容
        st.write("# Average Sleep health data:")
        st.write("You can compare your health data with the average value in the chosen chart")

        # Hard-coded user input data
        user_data = pd.DataFrame({'Age': [25], 'Sleep Duration': [7], 'Quality of Sleep': [6], 'BMI': ['Normal'], 'Sleep Disorder': ['None'], 'Occupation':['Software Engineer'], 'Stress Level': [4] })

        if uploaded_file is not None:
            # 使用缓存函数加载数据
            data = load_data(uploaded_file)

            # 显示图表选择器
            with st.sidebar:
                selected_chart = st.radio(
                    "Select a Chart",
                    options=["Age Distribution", "Sleep Duration vs Quality", "Occupation vs Sleep Quality", 
                            "BMI Category vs Heart Rate", "Stress Level vs Sleep Disorders"]
                )

            if selected_chart == "Age Distribution":
                plot_age_vs_sleep_quality(data, user_data)
            elif selected_chart == "Sleep Duration vs Quality":
                plot_sleep_duration_vs_quality(data, user_data)
            elif selected_chart == "Occupation vs Sleep Quality":
                plot_occupation_vs_sleep_quality(data)
            elif selected_chart == "BMI Category vs Heart Rate":
                plot_bmi_vs_heart_rate(data)
            elif selected_chart == "Stress Level vs Sleep Disorders":
                plot_stress_vs_sleep_disorders(data)

    elif selected == "Disease Prediction":
        st.header("Disease Prediction Module")
        st.write("Here you can implement models to predict diseases based on the uploaded dataset.")

if __name__ == "__main__":
    main()
