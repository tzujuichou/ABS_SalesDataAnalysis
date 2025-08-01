import streamlit as st
import pandas as pd 

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()