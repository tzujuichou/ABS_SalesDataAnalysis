import streamlit as st
import pandas as pd 
st.set_page_config(layout="wide")

from streamlit.components.v1 import html

# --- HIDE STREAMLIT BRANDING ---
hide_streamlit_branding = """
<style>
    #MainMenu {display: none;}
    header {display: none;}
</style>
"""
st.markdown(hide_streamlit_branding, unsafe_allow_html=True)

# Use the JavaScript snippet to hide the footer elements
html('''
    <script>
        var body = window.parent.document.querySelector(".main");
        var footer = body.querySelector("footer");
        if (footer) {
            footer.style.display = "none";
        }
    </script>
''')

pages = st.navigation([st.Page("Overview.py"), st.Page("Analysis.py")])
pages.run()