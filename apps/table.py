import streamlit as st
import pandas as pd
from data.load_data import crosses, plantlets, status, contamination, flowering, repeatpoll, summary
from helpers import download_csv

def app():
    st.title("Data Tables")

    col1, col2 = st.beta_columns(2)

    # column 1
    dataset = col2.selectbox('Dataset:', ('Crosses', 'Plantlets', 'Flowering','Status','Contamination'))

    if dataset == 'Crosses':
        dt = crosses()
    elif dataset == 'Plantlets':
        dt = plantlets()
    elif dataset == 'Flowering':
        dt = flowering()
    elif dataset == 'Status':
        dt = status()
    elif dataset == 'Contamination':
        dt = contamination()

    # column 2
    sites = dt['Location'].drop_duplicates().tolist()
    # sites.insert(0,'All')
    site = col1.selectbox('Site', sites)

    # column 3

    # Data table

    st.subheader(site + " - " + dataset)

    dt = [dt['Location'] == dataset]

    st.dataframe(dt)

    col3, col4 = st.beta_columns(2)
    col3.write('Number of entries: ' + str(dt.shape[0]))
    col4.markdown(download_csv(dt, 'Crossess'), unsafe_allow_html=True)

    # Summary Table
    st.header("Summary Table")
    aggr = st.multiselect('Aggregate By:', ['','Location','Mother','Father', 'Pollination_Year', 'Pollination_Month'])


    summarydt = summary()
    summarydt['Number_of_Crosses'] = 1
    if len(aggr) > 0:
        summarydt = summarydt.groupby(aggr, as_index=False).agg({
        "Number_of_Crosses" : "sum",
        "Total_Seeds": "sum",
        "Number_of_Embryo_Rescued": "sum",
        "Number_of_Embryo_Germinating": "sum",
        "Copies":  "sum",
        "Number_Rooting": "sum",
        "Number_Sent_Out": "sum",
        "Weaning_2_Plantlets": "sum",
        "Weaning_2_Plantlets": "sum",
        "Number_in_Screenhouse": "sum",
        "Number_in_Hardening": "sum",
        "Number_in_Openfield": "sum"
        })



    st.dataframe(summarydt)
    col5, col6 = st.beta_columns(2)
    col5.write('Number of entries: ' + str(summarydt.shape[0]))
    col6.markdown(download_csv(summarydt, 'Summary'), unsafe_allow_html=True)
