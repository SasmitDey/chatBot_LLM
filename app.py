import streamlit as st
from google import genai
from google.genai import types
from streamlit_chat import message
from pydantic import BaseModel


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

tools=[]
tools.append(types.Tool(google_search=types.GoogleSearch()))

#response structure
class Response(BaseModel):
    type: str
    data: str


def response(prompt:str):
    """
    Generates generator type object as a response to the provided input prompt

    Args:
    Prompt which is the message you want to send to the bot in the format of string

    Returns:
    Generator object (use write_stream)
    """
    response=chat.send_message_stream(
        message=prompt,
        config=types.GenerateContentConfig(
            tools=tools
        )
    )

    answer=""
    for chunk in response:
        answer+=chunk.text
    return answer








#streamlit app
st.set_page_config(
    page_title="Custom chatbot",
    page_icon="🗯",
    layout="wide"
)


#chat feature
# with st.chat_message(
#     name='ai',
#     width='stretch',
#     avatar='assistant'
# ):
#     prompt="Hey"
#     st.write_stream(response(prompt))
#     prompt = st.chat_input(
#         placeholder="enter message: ",  
#     )
#     st.write(f"User: {prompt}")
#     try:
#         st.write_stream(response(prompt))
#     except ValueError:
#         st.write("Hey")
    




#second chat design
def on_input_change():
    user_input = st.session_state.user_input
    if not user_input:
        st.warning("Please enter a message before sending.")
        return
    st.session_state.past.append(user_input)
    res=response(
        prompt=user_input
    )
    st.session_state.generated.append(res)
    st.session_state.user_input=""

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


# st.session_state.setdefault(
#     'past', 
#     []
# )
# st.session_state.setdefault(
#     'generated',
#     []
# )

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []



chat_placeholder = st.empty()


st.text_input(
    "Enter message: ",
    on_change=on_input_change,
    key='user_input'
)
st.session_state





# with chat_placeholder.container():    
#     for i in range(len(st.session_state['generated'])):                
#         message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
#         message(
#             st.session_state['generated'][i]['data'], 
#             key=f"{i}", 
#             allow_html=True,
#             is_table=True if st.session_state['generated'][i]['type']=='table' else False
#         )
    
#     # st.button("Clear message", on_click=on_btn_click)

# with st.container():
    # st.text_input("User Input:", on_change=on_input_change, key="user_input")