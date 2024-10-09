import streamlit as st
from langchain_community.chat_models import ChatOllama
st.set_page_config(page_title="질문하세요")
st.title("질문하세요")

def generate_response(input_text):
    llm = ChatOllama(
        model='Llama3.1:8b'
    )
    st.info(llm.invoke(input_text))

with st.form('Question'):
    text = st.text_area("질문 입력 : ", "What types of text models does Llama provide?")
    submitted = st.form_submit_button('보내기')
    generate_response(text)