import streamlit as st
from google import genai
from google.genai import types


gemini_api_key=st.secrets["model"]["gemini_api_key"]


try:
    client=genai.Client(
        api_key=gemini_api_key
    )
except Exception as e:
    print("Error getting gemini client")


chat = client.chats.create(
    model="models/gemini-2.5-flash-preview-05-20"
)





#streamlit app
st.set_page_config(
    page_title="Custom chatbot",
    page_icon="🗯",
    layout="wide"
)
