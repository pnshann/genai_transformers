import streamlit as st
from huggingface_hub import InferenceClient
from langchain import HuggingFaceHub
import requests
# Internal usage
import os
from time import sleep

#AVATARS
av_us = 'images/woman.png'  
av_bot = 'images/robot.png'

# FUNCTION TO LOG ALL CHAT MESSAGES INTO chathistory.txt
def writehistory(text):
    with open('chathistory.txt', 'a') as f:
        f.write(text)
        f.write('\n')
    f.close()

# Set HF API token
repo="HuggingFaceH4/starchat-beta"

### START STREAMLIT UI
st.title("Chatbot Powered by Hugging Face")
st.subheader("Starchat-beta Model")

with st.sidebar:
    yourHFtoken = st.text_input("HuggingFace API Key", key="yourHFtoken", type="password")
    "[Get an API Key from Hugging Face](https://huggingface.co/docs/hub/security-tokens)"
    "[View the source code](https://github.com/pnshann/genai_transformers/pages/2_Hugging_Face_Chatbot.py)"

# Set a default model
if "hf_model" not in st.session_state:
    st.session_state["hf_model"] = "HuggingFaceH4/starchat-beta"

### INITIALIZING STARCHAT FUNCTION MODEL
def starchat(model,myprompt, your_template):
    from langchain import PromptTemplate, LLMChain
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = yourHFtoken
    llm = HuggingFaceHub(repo_id=model , 
                         model_kwargs={"min_length":30,
                                       "max_new_tokens":256, "do_sample":True, 
                                       "temperature":0.2, "top_k":50, 
                                       "top_p":0.95, "eos_token_id":49155})
    template = your_template
    prompt = PromptTemplate(template=template, input_variables=["myprompt"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    llm_reply = llm_chain.run(myprompt)
    reply = llm_reply.partition('<|end|>')[0]
    return reply


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if myprompt := st.chat_input():
    if not yourHFtoken:
        st.info("Please add your HuggingFace API key to continue.")
        st.stop()
    
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = yourHFtoken
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(myprompt)
        usertext = f"user: {myprompt}"
        writehistory(usertext)
        # Display helper response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        res  =  starchat(
                st.session_state["hf_model"],
                myprompt, "<|system|>\n<|end|>\n<|user|>\n{myprompt}<|end|>\n<|assistant|>")
        response = res.split(" ")
        for r in response:
            full_response = full_response + r + " "
            message_placeholder.markdown(full_response + "▌")
            sleep(0.1)
        message_placeholder.markdown(full_response)
        helpertext = f"assistant: {full_response}"
        writehistory(helpertext)       
        st.session_state.messages.append({"role": "assistant", "content": full_response})