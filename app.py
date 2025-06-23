import streamlit as st
from google import genai
from google.genai import types
from streamlit_chat import message


gemini_api_key=st.secrets["model"]["gemini_api_key"]


try:
    client=genai.Client(
        api_key=gemini_api_key
    )
except Exception as e:
    print("Error getting gemini client")



# ----------configuring model----------
tools=[]
tools.append(types.Tool(google_search=types.GoogleSearch()))

system_instruction=st.secrets["model"]["system_instruction"]

config=types.GenerateContentConfig(
    tools=tools,
    system_instruction=system_instruction,
)
#----------configuration done----------

#model initialisation in streamlit using session states
if "chat" not in st.session_state:
    st.session_state.chat=client.chats.create(
        model="models/gemini-2.5-flash-preview-05-20"
    )


def get_response(prompt:str):
    """
    Generates generator type object as a response to the provided input prompt

    Args:
    Prompt which is the message you want to send to the bot in the format of string

    Returns:
    Generator object (use write_stream)
    """
    response=st.session_state.chat.send_message_stream(
        message=prompt,
        config=config
    )

    for chunk in response:
        yield chunk.text + " "



#streamlit app
st.set_page_config(
    page_title="Custom chatbot",
    page_icon="🗯",
    layout="wide"
)



#chat using native streamlit chat features

if "messages" not in st.session_state:
    st.session_state["messages"] = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])



if prompt:=st.chat_input("Enter message: "):
    st.chat_message('user').markdown(prompt)

    st.session_state.messages.append({"role":"user","message":prompt})

    # response = f"Bot: {get_response(prompt)}"

    with st.spinner("Thinking.."):
        try:
            with st.chat_message("assistant"):
                # with st.spinner("Thinking.."):
                response = st.write_stream(get_response(prompt=prompt))
                if 'happy birthday' in response.lower():
                    st.balloons()
            st.session_state.messages.append({"role": "assistant", "message": response})
        except Exception as e:
            with st.chat_message("assistant"):
                st.write(f"Error fetching response. Try again. Error-{e}")