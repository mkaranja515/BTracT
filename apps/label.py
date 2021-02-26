import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import plotly.express as px
from data.load_data import crosses, plantlets, status, contamination, flowering, repeatpoll, summary, label_data
from helpers import download_csv, to_excel

def app():
    st.title("Tissue Culture Labels")
    st.write("This page is for downloading pre-formatted data for generating barcode labels in TC labs")

    col1, col2 = st.beta_columns(2)
    labelType = col1.selectbox("Label Type", ('Crosses', 'Germinating Embryo','Subcultures','Rooting','Weaning1/ Sending Out', 'Weaning2','Screenhouse', 'Hardening','Openfield'))

    dt = label_data(labelType) # data

    dcol = dt.filter(regex='Date').columns
    lDate = col2.date_input("Date Range:", [])


    # show only relevant columns
    if labelType == 'Crosses':
        df = dt[['Location','Crossnumber','Embryo_Rescue_Date','Number_of_Embryo_Rescued']]
    else:
        df = dt.drop(['Prefix', 'Suffix', 'EmbryoNo'], axis = 1)

    # download only relevant columns
    if labelType == 'Crosses':
        dz = dt[['Crossnumber','Prefix','Suffix']]
    else:
        dz = dt[['PlantletID','Prefix','Suffix','EmbryoNo']]

    st.write(df)
    st.markdown(download_csv(dz, (labelType + " - " + str(datetime.now()))), unsafe_allow_html=True)
