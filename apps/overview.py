import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.load_data import crosses

def app():
    st.title("Overview")

    crosses1 = crosses() # dataset
    col1, col2 = st.beta_columns(2)

    overview_sites = crosses1['Location'].drop_duplicates().tolist() # sites
    overview_sites.insert(0,'')
    overview_site = col1.selectbox('Select Site', overview_sites)

    overview_dateRange = col2.date_input("Date Range:", [min(crosses1.First_Pollination_Date), max(crosses1.First_Pollination_Date)])

    # Histograms
    if len(overview_site) > 0:
        crosses1 = crosses1[crosses1['Location'] == overview_site]
    else:
        crosses1 = crosses1

    if len(overview_dateRange) > 0:
        mask = (crosses1['First_Pollination_Date'] > overview_dateRange[0]) & (crosses1['First_Pollination_Date'] <= overview_dateRange[1])
        crosses1 = crosses1.loc[mask]

    if len(overview_dateRange) > 0:
        ndays = abs((overview_dateRange[1] - overview_dateRange[0]).days)
        if ndays <= 31:
            crosses_count = crosses1.pivot_table(index=['Location','Day'], aggfunc='size')
        elif overview_dateRange[0].year == overview_dateRange[1].year:
            crosses_count = crosses1.pivot_table(index=['Location','Month'], aggfunc='size')
        elif overview_dateRange[0].year < overview_dateRange[1].year:
            crosses_count = crosses1.pivot_table(index=['Location','Year'], aggfunc='size')
    else:
         crosses_count = crosses1.pivot_table(index=['Location','Year'], aggfunc='size')


    crosses_count = pd.DataFrame(crosses_count)
    crosses_count.columns = ['N']
    crosses_count.reset_index(inplace=True)
    col = crosses_count.columns[1]
    crosses_count[col] = crosses_count[col].astype("category")

    # Infoboxes
    c1,c2,c3,c4,c5,c6 = st.beta_columns(6)

    st.text('')
    st.text('')
    c1.subheader(str(crosses1.shape[0]) + " Crosses")
    c2.subheader(str(crosses1.shape[0]) + " Bunches")
    c3.subheader(str(crosses1.shape[0]) + " Seeds")
    c4.subheader(str(crosses1.shape[0]) + " Embryos")
    c5.subheader(str(crosses1.shape[0]) + " Hardening")
    c6.subheader(str(crosses1.shape[0]) + " Openfield")
    st.text('')

    # total number of crosses
    st.markdown("<h2 style='text-align: center; color: orange;'>Total Number of Crosses</h2>", unsafe_allow_html=True)

    #fig1 = px.bar(crosses_count, x="Year", y="N",
    #            color=col, barmode='group',
    #            height=400)

    def bar_plot(df):
        fig = go.Figure()
        yrs = df['Year'].unique().tolist()
        years = [int(i) for i in yrs]
        loc = df['Location'].unique().tolist()
        dt = [pd.DataFrame(y) for x, y in df.groupby('Location', as_index=False)]
        colors = px.colors.qualitative.G10
        for i in range(len(dt)):
            L = loc[i]
            fig.add_trace(go.Bar(x=dt[i]['Year'],
                        y=dt[i]['N'],
                        name=L,
                        marker_color=colors[i]
                        ))

        fig.update_layout(
        #title='Total Number of Crosses',
        xaxis_tickfont_size=14,
        yaxis=dict(
        title='Number',
        titlefont_size=16,
        tickfont_size=14,
        ),
        legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return fig

    fig1 = bar_plot(crosses_count)
    st.plotly_chart(fig1)


    # female genotype
    female_count = crosses1["Mother"].value_counts().sort_values()

    st.markdown("<h2 style='text-align: center; color: orange;'>Female Genotype</h2>", unsafe_allow_html=True)
    st.bar_chart(female_count)
    st.write('Total number: ' + str(len(female_count)))

    # male genotype
    male_count = crosses1["Father"].value_counts().sort_values()

    st.markdown("<h2 style='text-align: center; color: orange;'>Male Genotype</h2>", unsafe_allow_html=True)
    st.bar_chart(male_count)
    st.write('Total number: ' + str(len(male_count)))

    # sunburst
    #data = dict(
    #character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    #parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    #value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

    #dt = pd.DataFrame(data)

    #fig =px.sunburst(
    #dt,
    #names='character',
    #parents='parent',
    #values='value',
    #)
    #fig.show()
