import streamlit as st
import joblib
import pandas as pd
import os


st.set_page_config(
    page_title='Predict',
    page_icon='',
    layout='wide'
)

if not os.path.exists("./data"):
    os.makedirs("./data")


st.cache_resource(show_spinner='Model Loading')
def load_forest_pipeline():
    pipeline = joblib.load('./models/forest_pipeline.joblib')
    return pipeline


st.cache_resource(show_spinner='Model Loading')
def load_scv_pipeline():
    pipeline = joblib.load('./models/svc_pipeline.joblib')
    return pipeline


st.cache_resource()
def select_model():
    col1, col2 = st.columns(2)

    with col1:
        st.selectbox('Select a Model', options=['Random Forest', 'SVC'], key='selected_model')
    with col2:
        pass

    if st.session_state['selected_model'] == 'Random Forest':
        pipeline = load_forest_pipeline()
    else:
        pipeline = load_scv_pipeline()

    encoder = joblib.load('./models/encoder.joblib')

    return pipeline, encoder


def make_prediction(pipeline, encoder):
    age = st.session_state['age']
    department = st.session_state['department']
    distancefromhome = st.session_state['distancefromhome']
    education = st.session_state['education']
    educational_field = st.session_state['educational_field']
    environmental_satisfaction = st.session_state['environmental_satisfaction']
    job_statisfaction = st.session_state['job_statisfaction']
    marital_status = st.session_state['marital_status']
    monthly_income = st.session_state['monthly_income']
    numofcompaniesworked = st.session_state['numofcompaniesworked']
    worklifebalance = st.session_state['worklifebalance']
    yearsatcompany = st.session_state['yearsatcompany']

    columns = ['Age', 'Department', 'DistanceFromHome', 'Education', 'EducationField',
       'EnvironmentSatisfaction', 'JobSatisfaction', 'MaritalStatus',
        'MonthlyIncome', 'NumCompaniesWorked', 'WorkLifeBalance',
        'YearsAtCompany']
    
    data = [[age, department, distancefromhome, education, educational_field, environmental_satisfaction, job_statisfaction, marital_status, monthly_income,
             numofcompaniesworked, worklifebalance,  yearsatcompany]]
    
    #create a dataframe
    df = pd.DataFrame(data, columns=columns)

    #Make prediction
    pred = pipeline.predict(df)
    prediction  = int(pred[0])
    prediction = encoder.inverse_transform([prediction])

    #Get probabilities
    probability = pipeline.predict_proba(df)

    #Updating state
    st.session_state['prediction'] = prediction
    st.session_state['probability'] = probability

    return prediction


def display_form():

    with st.spinner('Models Loading ...'):
        pipeline, encoder = select_model()

    with st.form('input-feature'):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write('### Personal Information')
            st.number_input('Enter age', min_value=18, max_value=60, step=1, key='age')
            st.number_input('Distance from Home', min_value=1, max_value=35, key='distancefromhome')
            st.number_input('Monthly Income', min_value=1000, step=100, key='monthly_income')
            st.selectbox('Marital Status', ['Single', 'Married', 'Divorced'], key='marital_status')
            

        with col2:
            st.write('### Work Information')
            st.selectbox('Enter department', options=['Sales', 'Research & Development', 'Human Resources'], key='department')
            st.selectbox('Enter Educational Field', options=['Life Sciences', 'Other', 'Medical', 'Marketing',
            'Technical Degree', 'Human Resources'], key='educational_field')
            st.number_input('Education', min_value=1, max_value=5, key='education')
            st.number_input("Years at company", min_value=1, key='yearsatcompany')

        with col3:
            st.write('### Satisfaction')
            st.number_input('Job Satisfaction', min_value=1, max_value=4, key='job_statisfaction')
            st.number_input('Environment Satisfaction', min_value=1, max_value=4, key='environmental_satisfaction')
            st.number_input('Work-Life Balance', min_value=1, max_value=4, key='worklifebalance')
            st.number_input('Num of Companies Worked At', min_value=1, max_value=4, key='numofcompaniesworked')

        st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))


if __name__ == "__main__":
    st.title("Make a Prediction")
    display_form()


    prediction = st.session_state['prediction']
    probability = st.session_state['probability']


    st.write(st.session_state)