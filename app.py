import streamlit as st
import pandas as pd 
st.set_page_config(layout="wide")

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {display: none;}
            header {display: none;}
            [data-testid="stFooter"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()