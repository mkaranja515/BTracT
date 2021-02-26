import streamlit as st
from multiapp import MultiApp
from apps import overview, table, label # import your app modules here

app = MultiApp()
#st.beta_set_page_title("BTracT")
# Add all your application here
app.add_app("OVERVIEW", overview.app)
app.add_app("DATA TABLE", table.app)
app.add_app("TISSUE CULTURE LABELS", label.app)

# The main app
app.run()
