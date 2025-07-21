import streamlit as st
from openai import OpenAI

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
    # header {visibility: hidden;}
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
#root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;padding-bottom: 1rem !important;}
.st-emotion-cache-1px2jnh { 
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
}
[data-testid="stBottomBlockContainer"] {
    background-color: aliceblue !important;
}
[data-testid="stChatInputTextArea"] {
    font-family: "Coming Soon", sans-serif !important;
}
</style>
<div>
</div>
""",
    unsafe_allow_html=True
)

st.write(" ")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title(""
"Hello! I'm your PocketDoctor! 🩺")
st.markdown(
    """
    <p style="text-align: center;">Tell me your questions and I'll do my best to assist you!</p>
    """, unsafe_allow_html=True)
# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
# Display previous messages
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])
# The  input
if prompt := st.chat_input("Ask me anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
    reply = response.choices[0].message.content
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})