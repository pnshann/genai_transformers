import streamlit as st

st.set_page_config(
    page_title="Hello!",
    page_icon="👋",
    layout = "wide"
)

st.write("# Welcome to Experimenting with Chatbots! 👋")

st.sidebar.success("Select from OpenAI or Hugging Face Above")

st.markdown(
    """
    This website was built for learning how to connect to various LLMs to create chatbots.

    **Select an interface from the sidebar 👈** to chat with a chatbot using either HuggingFace or OpenAI!
    """
)