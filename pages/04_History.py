import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='History',
    page_icon='',
    layout='wide'
)

st.title('Prediciton History')


def show_historic_predictions():
    
    csv_path = "./data/history.csv"
    df = pd.read_csv(csv_path)

    return df



if __name__ == "__main__":
    df = show_historic_predictions()
    st.dataframe(df)