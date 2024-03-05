import streamlit as st
import joblib
import pandas as pd
import os
import datetime


st.set_page_config(
    page_title='Predict',
    page_icon='',
    layout='wide'
)


@st.cache_resource(show_spinner='Models Loading')
def load_forest_pipeline():
    pipeline = joblib.load('./models/forest_pipeline.joblib')
    return pipeline


@st.cache_resource(show_spinner='Models Loading')
def load_scv_pipeline():
    pipeline = joblib.load('./models/svc_pipeline.joblib')
    return pipeline


def select_model():
    col1, col2 = st.columns(2)

    with col1:
        st.selectbox('Select a Model', options=[
                     'Random Forest', 'SVC'], key='selected_model')
    with col2:
        pass

    if st.session_state['selected_model'] == 'Random Forest':
        pipeline = load_forest_pipeline()
    else:
        pipeline = load_scv_pipeline()

    encoder = joblib.load('./models/encoder.joblib')

    return pipeline, encoder


if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

if 'probability' not in st.session_state:
    st.session_state['probability'] = None



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

    # create a dataframe
    df = pd.DataFrame(data, columns=columns)

    df['Prediciton Time'] = datetime.date.today()
    df['Model Used'] = st.session_state['selected_model']

    df.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

    # Make prediction
    pred = pipeline.predict(df)
    pred = int(pred[0])
    prediction = encoder.inverse_transform([pred])

    # Get probabilities
    probability = pipeline.predict_proba(df)

    # Updating state
    st.session_state['prediction'] = prediction
    st.session_state['probability'] = probability

    return prediction, probability




def display_form():

    pipeline, encoder = select_model()

    with st.form('input-feature'):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write('### Personal Information')
            st.number_input('Enter age', min_value=18,
                            max_value=60, step=1, key='age')
            st.number_input('Distance from Home', min_value=1,
                            max_value=35, key='distancefromhome')
            st.number_input('Monthly Income', min_value=1000,
                            step=100, key='monthly_income')
            st.selectbox('Marital Status', [
                         'Single', 'Married', 'Divorced'], key='marital_status')

        with col2:
            st.write('### Work Information')
            st.selectbox('Enter department', options=[
                         'Sales', 'Research & Development', 'Human Resources'], key='department')
            st.selectbox('Enter Educational Field', options=['Life Sciences', 'Other', 'Medical', 'Marketing',
                                                             'Technical Degree', 'Human Resources'], key='educational_field')
            st.number_input('Education', min_value=1,
                            max_value=5, key='education')
            st.number_input("Years at company", min_value=1,
                            key='yearsatcompany')

        with col3:
            st.write('### Satisfaction')
            st.number_input('Job Satisfaction', min_value=1,
                            max_value=4, key='job_statisfaction')
            st.number_input('Environment Satisfaction', min_value=1,
                            max_value=4, key='environmental_satisfaction')
            st.number_input('Work-Life Balance', min_value=1,
                            max_value=4, key='worklifebalance')
            st.number_input('Num of Companies Worked At', min_value=1,
                            max_value=4, key='numofcompaniesworked')

        st.form_submit_button('Make Prediction', on_click=make_prediction, kwargs=dict(
            pipeline=pipeline, encoder=encoder))


if __name__ == "__main__":
    st.title("Make a Prediction")
    display_form()

    prediction = st.session_state['prediction']
    probability = st.session_state['probability']

    if not prediction:
        st.markdown("### Predictions will show here")
    elif prediction == "Yes":
        probability_of_yes = probability[0][1] * 100
        st.markdown(f"### The employee will leave the company with a probability of {round(probability_of_yes, 2)}%")
    else:
        probability_of_no = probability[0][0] * 100
        st.markdown(f"### Employee will not leave the company with a probability of  {round(probability_of_no, 2)}%")

    # st.write(st.session_state)