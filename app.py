import streamlit as st
import pandas as pd 
st.set_page_config(layout="wide")

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer {
            visibility: hidden;
                }
            footer:after {
                content:'goodbye'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
            }
            [data-testid="stStatusWidget"] {display: none;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()