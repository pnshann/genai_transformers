import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init():
    # setup streamlit page
    st.set_page_config(
        page_title="Chatbot Powered by OpenAI"
    )

    st.header("Your personal chatbot! Powered by OpenAI")
    
    with st.sidebar:
      youropenaikey = st.text_input("OpenAI API Key", key="youropenaitoken", type="password")    

    if not youropenaikey:
      st.info("Please add your OpenAI API key to continue.")
      st.stop()
    
    os.environ["OPENAI_API_KEY"] = youropenaikey


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            # this is our prompt template that we are using 
            SystemMessage(content="You are a helpful assistant.")
        ]

    user_input = st.text_input("Your message: ", key="user_input")

    # handle user input
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(
	    # AIMessage is acting as our output parser 
            AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()