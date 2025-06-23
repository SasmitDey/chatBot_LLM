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

#model initialisation
chat = client.chats.create(
    model="models/gemini-2.5-flash-preview-05-20"
)

#configuring model
tools=[]
tools.append(types.Tool(google_search=types.GoogleSearch()))

system_instruction=st.secrets["model"]["system_instruction"]

config=types.GenerateContentConfig(
    tools=tools,
    system_instruction=system_instruction,
)
#configuration done


def get_response(prompt:str):
    """
    Generates generator type object as a response to the provided input prompt

    Args:
    Prompt which is the message you want to send to the bot in the format of string

    Returns:
    Generator object (use write_stream)
    """
    response=chat.send_message_stream(
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



#chat
# def on_input_change():
#     user_input = st.session_state.user_input
#     if not user_input:
#         st.warning("Please enter a message before sending.")
#         return
#     st.session_state.past.append(user_input)
#     res=response(
#         prompt=user_input
#     )
#     st.session_state.generated.append(res)
#     st.session_state.user_input=""

# def on_btn_click():
#     del st.session_state.past[:]
#     del st.session_state.generated[:]


# #adding session states
# if 'user_input' not in st.session_state:
#     st.session_state['user_input'] = ''

# if 'past' not in st.session_state:
#     st.session_state['past'] = []

# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []
# #session states added



# with st.container():
#     for i in range(len(st.session_state['generated'])):
#         message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
#         message(
#             st.session_state['generated'][i],
#             key=f"{i}",
#             allow_html=True
#         )


# with st.container():
#     st.text_input("User Input: ", on_change=on_input_change, key="user_input")


#testing native streamlit chat features


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
        except Exception:
            with st.chat_message("assistant"):
                st.write("Error fetching response. Try again.")