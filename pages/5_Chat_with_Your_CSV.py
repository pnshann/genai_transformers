from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import pandas as pd
import os
import streamlit as st
import tempfile


def main():
    load_dotenv()

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    with st.sidebar:
      youropenaikey = st.text_input("OpenAI API Key", key="youropenaitoken", type="password")    
      csv_file = st.file_uploader("Upload a CSV file", type="csv")

    if not youropenaikey:
      st.info("Please add your OpenAI API key to continue.")
      st.stop()
    
    os.environ["OPENAI_API_KEY"] = youropenaikey
    
    if csv_file is not None:
        file_path = os.path.join("../",csv_file.name)
        with open(file_path, "wb") as f:
            f.write(csv_file.getbuffer())
        
        df = pd.read_csv(file_path)
        st.dataframe(df)

    if csv_file is not None:

        # create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temporary_file:
            temporary_file.write(csv_file.getvalue())

        # initialize agent
        agent = create_csv_agent(OpenAI(temperature=0, model_name = 'gpt-3.5-turbo-16k'), path=temporary_file.name, verbose=True)

        # delete temp file
        os.unlink(temporary_file.name)

        user_question = st.text_input("Ask a question about your CSV: ")

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                st.write(agent.run(user_question))


if __name__ == "__main__":
    main()