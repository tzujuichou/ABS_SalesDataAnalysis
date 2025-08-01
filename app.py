import streamlit as st
import pandas as pd 

hide_toolbar_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_toolbar_style, unsafe_allow_html=True)

pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()