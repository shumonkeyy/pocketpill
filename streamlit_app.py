import altair as alt
import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
import os

st.set_page_config(layout="wide")

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Gamja+Flower&display=swap" rel="stylesheet">')
st.markdown(
    """
<style>
.stApp {
    background-color: aliceblue; /* Replace with your desired color */
    text-align: start;
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
}
</style>
<h1 style="text-align: center;font-family: "Gamja Flower", sans-serif;>PocketPill</h1>
""",
    unsafe_allow_html=True
)

if "data_entered" not in st.session_state:
    st.session_state.data_entered = False

side_effects_data = pd.read_csv("data/medicine_dataset.csv").drop_duplicates()
sorted_data = side_effects_data[[
    "name", "substitute0", "substitute1", "substitute2", "sideEffect0", "sideEffect1", "sideEffect2"
]]

df = pd.read_csv("data/drugsComTrain_raw.csv")
df = df.dropna(subset=["condition"])
df = df[~df["condition"].str.contains("users found this comment helpful", case=False, na=False)]
df = df[df["condition"] <= "Zollinger-Ellison Syndrome"]
df = df.drop(columns=["review", "date"])
df = df.drop(columns=df.columns[:1])
df = df.reset_index(drop=True)
conditions = sorted(df["condition"].unique())

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.write("Fill this out!")
        patient_name = st.text_input("Name:")
        patient_age = st.text_input("Age:")
        patient_gender = st.text_input("Gender:")
        selected_condition = st.selectbox("Choose a condition to filter by:", conditions)
        if st.button("Submit"):
            st.session_state.data_entered = True
    with st.container(border=True):
        st.write("Instructions for PillPocket")

with col2:
    if st.session_state.data_entered==True:
        with st.container(border=True,height=500):
            filtered_df = df[df["condition"] == selected_condition]
            sort_option = st.radio(
                "Sort reviews by:",
                options=["usefulCount", "rating"],
                index=0,
                horizontal=True
                )
            filtered_df = filtered_df.sort_values(by=sort_option, ascending=False)
            st.write(f"Showing reviews for: **{selected_condition}** (sorted by **{sort_option}**)")
            st.dataframe(filtered_df.head(10))

with col3:
    if st.session_state.data_entered==True:
        with st.container(border=True):
            st.write("Medical Side Effects and Remedies")
            medication_input = st.text_input("Your Medication").lower()
            if medication_input:
                filtered_name = sorted_data[sorted_data['name'].str.lower().str.contains(medication_input)]
                st.write("Side Effects:")
                st.write(filtered_name[["sideEffect0", "sideEffect1", "sideEffect2"]].drop_duplicates())
                st.write("Substitutes")
                st.write(filtered_name[["substitute0"]].drop_duplicates())


