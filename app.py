import streamlit as st
import pandas as pd 

pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()