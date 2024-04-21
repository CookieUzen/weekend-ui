import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time


# 使用st.cache装饰器来缓存加载的数据
@st.cache_resource
def load_data(uploaded_file='./Sleep_health_and_lifestyle_dataset.csv'):
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
