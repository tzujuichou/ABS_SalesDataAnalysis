import streamlit as st
import pandas as pd 

# hide_specific_elements_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             button[title="View app menu"] {visibility: hidden;}
#             div[data-testid="stToolbar"] {
#                 display: flex;
#                 justify-content: flex-end; 
#             }
#             footer {visibility: hidden;}
#             </style>
#             """

hide_elements_style = """
            <style>
            div[data-testid="stToolbar"] {
                right: 2rem;
            }

            div[data-testid="stToolbar"] > button[title="View app menu"] {
                display: none;
            }
            
            div[data-testid="stToolbar"] > button[title="Fork"] {
                display: none;
            }

            div[data-testid="stToolbar"] > a {
                display: none;
            }

            footer {
                display: none;
            }
            </style>
            """
st.markdown(hide_elements_style, unsafe_allow_html=True)


pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()