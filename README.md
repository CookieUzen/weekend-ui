# Predictive Modeling for Health Conditions
## Project Overview 😇
This project utilizes machine learning techniques to predict the likelihood of developing heart disease, mental health issues, asthma, and skin cancer. By analyzing relavant columns, our models aim to provide early warnings to individuals at risk, thereby supporting preventive healthcare measures.

## Inspiration
The motivation behind this project was to leverage the power of data science and machine learning to make a tangible difference in people's lives by predicting severe health conditions before they become critical. The ability to predict these conditions can facilitate early intervention and potentially save lives.

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

# Authors 🫡
Uzen, Tommy, Tina, Annie. Hats off to you!

## Acknowledgments 😊
Thanks to all the public datasets that allowed us to learn and play around. Specifically, we use 

## What it does 🤔
Our application inputs user data such as demographic details, lifestyle information, and basic medical history to predict the likelihood of developing specific health conditions. This tool is designed to be used by healthcare professionals to identify at-risk patients and possibly intervene earlier than usual.

## How we built it 
We built this project using Python for data processing and machine learning, employing libraries such as Pandas, scikit-learn, and TensorFlow for more complex model implementations. The user interface was created using Streamlit, which allowed us to quickly develop and deploy an interactive web application.

## Research 📚
Our research began with a thorough review of medical journals and consultation with healthcare professionals to identify key indicators of each health condition. This informed our data collection and feature selection, ensuring our model's relevance to real-world scenarios.

## Design 
The design of our application focuses on usability, ensuring that healthcare professionals can easily input data and interpret model predictions. The interface is clean, intuitive, and accessible, designed to be used in busy clinical environments without requiring extensive training.

## Challenges we ran into 😰
We encountered challenges in dealing with imbalanced data, as some health conditions were significantly underrepresented. This was addressed by implementing advanced sampling techniques and adjusting model evaluation metrics to focus on sensitivity and specificity.

## Accomplishments that we're proud of 🥲
We are proud of developing a model that not only achieves high accuracy but also adheres to ethical standards in AI, ensuring our predictions are as unbiased as possible. Additionally, seeing our application being potentially used in clinical settings has been incredibly fulfilling.

## What we learned 🤗
Throughout this project, we've gained a deeper understanding of machine learning applications in healthcare, the importance of meticulous data preprocessing, and the ethical implications of predictive modeling. We also learned the value of interdisciplinary collaboration, combining insights from data science, medicine, and UX design!
