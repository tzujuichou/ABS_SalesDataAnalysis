import streamlit as st
import pandas as pd 

hide_specific_elements_style = """
            <style>
            #MainMenu {visibility: hidden;}
            button[title="View app menu"] {visibility: hidden;}
            div[data-testid="stToolbar"] {
                display: flex;
                justify-content: flex-end; 
            }
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_specific_elements_style, unsafe_allow_html=True)


pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()