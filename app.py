import streamlit as st
import pandas as pd 
st.set_page_config(layout="wide")

# The comprehensive CSS from the Streamlit community to hide all branding
hide_st_style = """
            <style>
            /* Hide the Streamlit logo */
            div[data-testid="stToolbar"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
            }
            /* Hide the decoration line */
            div[data-testid="stDecoration"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
            }
            /* Hide the footer which contains "Manage app" */
            div[data-testid="stStatusWidget"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
            }
            /* Hide the hamburger menu */
            #MainMenu {
            visibility: hidden;
            height: 0%;
            }
            /* Hide the header */
            header {
            visibility: hidden;
            height: 0%;
            }
            /* Hide the footer text */
            footer {
            visibility: hidden;
            height: 0%;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()