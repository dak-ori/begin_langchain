import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# PDF에서 텍스트를 추출
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# 조건에 맞게 텍스트를 더 작은 청크로 분할
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n'],
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# 텍스트 청크에 대한 임베딩을 생성하고 FAISS를 사용해서 벡터저장소를 생성
def get_vectorstore(text_chunks):
    EMBEDDINGS = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding=EMBEDDINGS)
    return vectorstore

# 벡터 저장소로 대화 체인을 초기화
def get_conversation_chain(vectorstore):
    # 이전 대화 저장
    memory = ConversationBufferWindowMemory(memory_key='chat_history', return_messages=True)
    
    # 랭체인 챗봇에 쿼리 저장
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOllama(model='llama3.1:8b'), 
        retriever=vectorstore.as_retriever(),
        get_chat_history=lambda h: h,
        memory=memory
    )
    return conversation_chain

user_uploads = st.file_uploader("파일을 업로드하세요.", accept_multiple_files=True)
if user_uploads is not None:
    if st.button("Upload"):
        with st.spinner("처리중.."):
            # PDF 텍스트 가져오기
            raw_text = get_pdf_text(user_uploads)
            # 텍스트에서 청크검색
            text_chunks = get_text_chunks(raw_text)
            # PDF 텍스트 저장을 위해 파이스 벡터 저장소 새성
            vectorstore = get_vectorstore(text_chunks)
            # 대화 체인 만들기
            st.session_state.conversation = get_conversation_chain(vectorstore)
            
if user_query := st.chat_input("질문을 입력하세요."):
    if 'conversation' in st.session_state:
        result = st.session_state.conversation({
            "question" : user_query,
            "chat_history" : st.session_state.get('chat_history', [])
        })
        response = result["answer"]
    else:
        response = "먼저 문서를 업로드하세요."
    with st.chat_message("assistant"):
        st.write(response)