import streamlit as st
import pandas as pd 

hide_specific_elements_style = """
            <style>
            /* Hide the hamburger menu */
            #MainMenu {visibility: hidden;}
            button[title="View app menu"] {visibility: hidden;}

            /* Hide the GitHub and Fork buttons */
            div[data-testid="stToolbar"] {
                display: flex;
                justify-content: flex-end; /* Aligns remaining items to the right */
            }
            div[data-testid="stToolbar"] a[title="View on GitHub"] {
                display: none;
            }
            div[data-testid="stToolbar"] button[title="Fork"] {
                display: none;
            }

            /* Hide the footer */
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_specific_elements_style, unsafe_allow_html=True)


pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()