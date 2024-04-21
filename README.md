# Predictive Modeling for Health Conditions
## Project Overview 😇
Do you have skin cancer? This project creates a website that utilizes machine learning techniques to predict an individual's likelihood of developing several diseases, such as heart disease, diabetes, and asthma. By analyzing relevant lifestyle data, our models aim to provide early warnings to individuals at risk, thereby supporting preventive healthcare measures and improving public health outcomes. 

This is the project for Caltech Hackathon 2024. 

### Problem Statement
We built a website that uses a machine learning model that takes in personal health data to predict and estimate the user's risk of certain diseases. 

## Inspiration 😋

We've chosen our theme and topic based on a pressing issue observed in recent years: the increasing prevalence of illnesses among the parental generation. Many diseases are preventable if they are diagnosed early and promptly tackled by clinical interventions and lifestyle changes. However, early diagnosis is often challenging as diseases can be asymptomatic in their initial stages. This creates a need for a model that can identify individuals at risk for certain conditions before symptoms appear. At the same time, the intersection of machine learning and healthcare has opened new avenues for predictive diagnostics. Conditions like heart disease, asthma, and diabetic are major contributors to morbidity and mortality worldwide. The ability to predict these conditions can facilitate public health and potentially save lives. 

This motivates us to create this project, which focuses on using predictive modeling to forecast the likelihood of major health conditions that significantly impact global health, and making such predictions easily accessible for everyone by building a website with a simple user interface.

## Features 🤩
Comprehensive Data Analysis: Utilization of statistical analysis and data visualization to select and engineer features. 

Advanced Predictive Modeling: Implementation of multiple machine learning algorithms to optimize prediction accuracy.

Iterative Testing and Refinement: Continuous model improvement based on feedback and new data.

## Getting Started 🫥
Quickly get the project up and running with `poetry`:
```bash
poetry run streamlit run Main_Page.py
```

A Dockerfile is included if you want to deploy the website yourself!

```bash
docker build . -t app
docker run -p 80:8501 app
```

Note that the website runs in debug mode by default.
Set `DEBUG=false` in your environment to disable debug logs.
This is already done in the Dockerfile.

## What it does 🤔
Our application inputs user data such as demographic details, lifestyle information, and basic medical history to predict the likelihood of developing specific health conditions. 
This tool is designed to be used by healthcare professionals to identify at-risk patients and possibly intervene earlier than usual. 

## How we built it 🫕
We built this project using Python for data processing and machine learning, employing libraries such as Pandas, scikit-learn, and xgBoost (&& !Tensorflow) for more complex model implementations. The user interface was created using Streamlit, which allowed us to quickly develop and deploy an interactive web application.

## Research 📚
Our research began with a thorough review of medical journals and consultation with healthcare professionals to identify key indicators of each health condition. 
This informed our data collection and feature selection, ensuring our model's relevance to real-world scenarios.

## Design 🍡
The design of our application focuses on usability, ensuring that healthcare professionals can easily input data and interpret model predictions. The interface is clean, intuitive, and accessible, designed to be used in busy clinical environments without requiring extensive training.

## Challenges we ran into 😰
1. Model Deployment: During the model deployment phase, the model behaved unexpectedly when integrated into our website. We addressed this by adding a preprocessing module to handle user inputs more effectively. 
2. In designing the model, we considered the problem that most datasets will not each have the data input we want. After trying different datasets, we solved this problem by using a huge dataset and data preprocessing.
3. Communication: Since its our first Hackathon, we did not have a good idea how to organize our tasks. As a result we had issues with communication and assigning tasks. Sometimes we had problems overlapping work which cause time to be wasted, or changes in code that broke old code.

## Accomplishments that we're proud of 🥲
We are proud of developing a model that not only achieves high accuracy but also has practical application in our daily life.
Additionally, we are proud of learning to write frontend in a day!

## What we learned 🤗
Throughout this project, we've gained a deeper understanding of machine learning applications in healthcare, the importance of data preprocessing, and the ethical implications of predictive modeling. We also learned the value of interdisciplinary collaboration, combining insights from data science, medicine, and UX design! 

## Authors 🫡
Uzen, Tommy, Tina, Annie.

## Acknowledgments 😊
Thanks to all the public datasets that allowed us to learn and play around. Specifically, we utilized health data sets from 
https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease/data. 
Additionally, [streamlit](https://streamlit.io/) helped us make the ui development process easy.
