import altair as alt
import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
import os

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Coming+Soon&display=swap');
    </style>
    """, unsafe_allow_html=True)
            
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
h1 {
    text-align: center;
    font-family: "Gamja Flower", sans-serif !important;
    color: black !important;
}
p {
    font-family: "Coming Soon", sans-serif !important;
    color: black !important;
}
button {
    background-color: white !important;
    border: 1px solid black !important;
}
button:hover {
    border: 1px solid #748DAE !important;
    transition: 1s;
}
.st-key-stickynote1 {
    background-color: #9ECAD6 !important;
}
.st-key-stickynote2 {
    background-color: #FFE8CD !important;
}
.st-key-stickynote3 {
    background-color: #FFEAEA !important;
}
.st-key-stickynote4 {
    background-color: #D1D8BE !important;
}
#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;padding-bottom: 1rem !important;}
.st-emotion-cache-1px2jnh { 
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
    }
</style>
<h1>PocketPill</h1>
""",
    unsafe_allow_html=True
)

if "data_entered" not in st.session_state:
    st.session_state.data_entered = False

@st.cache_data
def load_side_effects():
    return pd.read_csv("data/medicine_dataset.csv").drop_duplicates()
side_effects_data = load_side_effects()

@st.cache_data
def load_sorted_side_effects():
    return side_effects_data[[
        "name", "substitute0", "substitute1", "substitute2", "sideEffect0", "sideEffect1", "sideEffect2"
        ]]
sorted_data = load_sorted_side_effects()

@st.cache_data
def clean_side_effects():
    side_effects_data["name"] = side_effects_data["name"].str.split().str[0]
    return side_effects_data["name"].drop_duplicates()
clean_name = clean_side_effects()


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
    with st.container(key="stickynote1", border=True):
        st.write("Fill this out!")
        st.text_input("Name:")
        st.text_input("Age:")
        st.text_input("Gender:")
        selected_condition = st.selectbox("Choose a condition to filter by:", conditions, placeholder="Select Condition")
        if st.button("Submit"):
            st.session_state.data_entered = True
    with st.container(key="stickynote2", border=True):
        st.write("Instructions for PillPocket")
        st.write("Tell us about yourself. Browse recommended medications tailored to you. Research drugs thoroughly before requesting a formal prescription, or purchasing a non-prescription medication.")

with col2:
    if st.session_state.data_entered==True:
        with st.container(key="stickynote3", border=True):
            filtered_df = df[df["condition"] == selected_condition]
            sort_option = st.radio(
                "Sort reviews by:",
                options=["usefulCount", "rating"],
                index=0,
                horizontal=True
                )
            filtered_df = filtered_df.sort_values(by=sort_option, ascending=False).reset_index(drop=True)
            st.write(f"Showing reviews for: **{selected_condition}** (sorted by **{sort_option}**)")
            st.dataframe(filtered_df.head(10))

with col3:
    if st.session_state.data_entered==True:
        with st.container(key="stickynote4", border=True):
            st.write("Medical Side Effects and Substitutes")
            medication_input = st.selectbox("Generic (non-brand) Name of Your Medication", clean_name)
            if medication_input:
                filtered_name = sorted_data[sorted_data['name'].str.lower().str.contains(medication_input)]
                st.write("Side Effects:")
                st.write(filtered_name[["sideEffect0", "sideEffect1", "sideEffect2"]].drop_duplicates())
                st.write("Substitutes")
                st.write(filtered_name[["substitute0"]].drop_duplicates())


