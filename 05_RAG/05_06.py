from langchain import LLMChain
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os

langs = ["korean", "Japanese", "Chinese", "English"]
left_co, cent_co, last_co = st.columns(3)

with st.sidebar:
    language = st.radio("번역을 원하는 언어를 선택하시오.", langs)

st.markdown("언어 번역 서비스")
prompt = st.text_input("번역을 원하는 텍스트를 입력하시오.")

trans_template = PromptTemplate(
    input_variables=["trans"],
    template="Your task is to translate this text to " + language + 'TEXT: {trans}'
)

memory = ConversationBufferMemory(input_key='trans', memory_key='chat_history')

llm = ChatOpenAI(temperature=0.0, model='gpt-4o')
trans_chain = LLMChain(llm=llm, prompt=trans_template, verbose = True, output_key = 'translate', memory= memory)

if st.button("번역"):
    if prompt:
        response = trans_chain({'trans' : prompt})
        st.info(response['translate'])