import altair as alt
import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from deep_translator import GoogleTranslator
# -------------------------------
# :globe_with_meridians: Language translation setup
# -------------------------------
language_dict = GoogleTranslator().get_supported_languages(as_dict=True)
default_language_name = 'english'

# -------------------------------
# Page styling and theme
# -------------------------------
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Coming+Soon&display=swap');
    .stApp {
        background-color: aliceblue;
        text-align: start;
    }
    h1 {
        text-align: center !important;
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
    .st-key-stickynote5 {
        background-color: #FFD6BA !important;
    }
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
    }
    </style>
    """, unsafe_allow_html=True
)
# -------------------------------
# Header
# -------------------------------
st.markdown(f"<h1>PocketPill 💊</h1>", unsafe_allow_html=True)

# -------------------------------
# Language translation selection
# -------------------------------
selected_lang_name = st.selectbox(
    "🌐 Choose a language",
    options=list(language_dict.keys()),
    index=list(language_dict.keys()).index(default_language_name)
)
selected_lang_code = language_dict[selected_lang_name]
translations = {
    "title": "PocketPill",
    "instruction_title": "Instructions for PocketPill",
    "instruction_body": (
        "Tell us about yourself. Browse recommended medications tailored to you. "
        "Research drugs thoroughly before requesting a formal prescription, or purchasing a non-prescription medication."
    ),
    "select_condition": "Choose a condition to filter by:",
    "side_effects_title": "Top Side Effects",
    "sort_reviews": "Sort reviews by:",
    "reviews_for": "Showing reviews for",
    "side_effects": "Side Effects",
    "substitutes": "Substitutes",
    "medical_info": "Medical Side Effects and Substitutes",
    "select_med": "Generic (non-brand) Name of Your Medication",
    "medbot_title": "Hi I'm MedBot",
    "ask_medbot": "Ask me anything...",
    "no_data": "No data found for the given medicine.",
}
@st.cache_data(show_spinner=False)
def translate_texts(target_lang):
    if target_lang == "en":
        return translations.copy()
    translated = {}
    for key, val in translations.items():
        try:
            translated[key] = GoogleTranslator(source='en', target=target_lang).translate(val)
        except Exception:
            translated[key] = val
    return translated
t = translate_texts(selected_lang_code)
# -------------------------------
# Load & clean data
# -------------------------------
@st.cache_data
def load_side_effects():
    return pd.read_csv("data/medicine_dataset.csv").drop_duplicates()
side_effects_data = load_side_effects()
bar_chart_data = side_effects_data.copy()
@st.cache_data
def load_sorted_side_effects():
    return side_effects_data[[
        "name", "substitute0", "substitute1", "substitute2",
        "sideEffect0", "sideEffect1", "sideEffect2"
    ]]
sorted_data = load_sorted_side_effects()
@st.cache_data
def clean_side_effects(df):
    df["name"] = df["name"].str.split().str[0]
    return df[df["name"].apply(lambda x: len(str(x)) > 3)]["name"].drop_duplicates()
clean_name = clean_side_effects(side_effects_data)
df = pd.read_csv("data/drugsComTrain_raw.csv")
df = df.dropna(subset=["condition"])
df = df[~df["condition"].str.contains("users found this comment helpful", case=False, na=False)]
df = df[df["condition"] <= "Zollinger-Ellison Syndrome"]
df = df.drop(columns=["review", "date"] + list(df.columns[:1]))
df = df.reset_index(drop=True)
df = df.drop_duplicates(subset=["drugName", "condition"])
conditions = sorted(df["condition"].unique())
# -------------------------------
# Bar chart data
# -------------------------------
side_effect_cols = [col for col in bar_chart_data.columns if 'sideeffect' in col.lower()]
all_effects = []
for col in side_effect_cols:
    all_effects += bar_chart_data[col].dropna().astype(str).str.capitalize().tolist()
side_effect_counts = Counter(all_effects)
side_df = pd.DataFrame(side_effect_counts.items(), columns=["Side Effect", "Count"])
side_df_top = side_df.sort_values(by="Count", ascending=False).head(20)
# -------------------------------
# Layout
# -------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(key="stickynote1", border=True):
        st.write(f"{t['instruction_title']}")
        st.write(t["instruction_body"])
    with st.container(key="stickynote2", border=True):
        selected_condition = st.selectbox(t["select_condition"], conditions)
        if selected_condition:
            st.session_state.data_entered = True
    with st.container(key="stickynote5", border=True):
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(data=side_df_top, y="Side Effect", x="Count", palette="bone", ax=ax)
        ax.set_title(t["side_effects_title"])
        ax.set_xlabel("Occurrences")
        ax.set_ylabel(t["side_effects"])
        st.pyplot(fig)
with col2:
    with st.container(key="stickynote3", border=True):
        if st.session_state.get("data_entered"):
            filtered_df = df[df["condition"] == selected_condition]
            sort_option = st.radio(t["sort_reviews"], ["usefulCount", "rating"], index=0, horizontal=True)
            filtered_df = filtered_df.sort_values(by=sort_option, ascending=False).reset_index(drop=True)
            st.write(f"{t['reviews_for']}: **{selected_condition}** (sorted by **{sort_option}**)")
            st.dataframe(filtered_df.head(10))
with col3:
    with st.container(key="stickynote4", border=True):
        st.write(t["medical_info"])
        medication_input = st.selectbox(t["select_med"], clean_name)
        if medication_input:
            filtered_name = sorted_data[sorted_data["name"].str.lower().str.contains(medication_input.lower())]
            if not filtered_name.empty:
                st.write(f"{t['side_effects']}:")
                st.write(filtered_name[["sideEffect0", "sideEffect1", "sideEffect2"]].drop_duplicates().reset_index(drop=True).head(1))
                st.write(t["substitutes"])
                st.write(filtered_name[["substitute0"]].drop_duplicates().reset_index(drop=True).head())
            else:
                st.warning(t["no_data"])