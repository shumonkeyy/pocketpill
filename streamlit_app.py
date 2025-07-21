import altair as alt
import pandas as pd
import streamlit as st

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: white !important;
    font-family: "Gamja Flower", sans-serif !important;
    font-size: 40px !important;
}
</style>
""", unsafe_allow_html=True)

pages = {
    "PocketPages":
    [
        st.Page("pages/home.py", title="PocketPill"),
        st.Page("pages/chatbot.py", title="PocketDoctor")
    ]
}
pg = st.navigation(pages)
pg.run()