# from PyPDF2 import PdfReader
# import streamlit as st
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_community.chat_models import ChatOllama
# from langchain_community.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain_huggingface import HuggingFaceEmbeddings

# def process_text(text):
#     text_splitter = CharacterTextSplitter(
#         separator='\n',
#         chunk_size=1000,
#         chunk_overlap=20,
#         length_function=len,
#     )
#     chunks = text_splitter.split_text(text)
    
#     embeddings = HuggingFaceEmbeddings(model_name = "intfloat/multilingual-e5-small")
#     documents = FAISS.from_texts(chunks, embeddings)
#     return documents

# def main():
#     st.title("PDF 요약하기")
#     st.divider()
    
#     pdf = st.file_uploader('PDF파일을 업로드하세요', type='pdf')
    
#     if pdf is not None:
#         pdf_reader = PdfReader(pdf)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text()
        
#         documents = process_text(text)
#         query = "업로드된 PDF 파일의 내용을 5문장으로 요약해주세요"
        
#         if query:
#             docs = documents.similarity_search(query)
#             llm = ChatOllama(model='llama3.1:8b')
#             chain = load_qa_chain(llm, chain_type='stuff')
            
#             response = chain.invoke({"input_documents" : docs, "question" : query})
            
#             st.subheader("--요약 결과--")
#             st.write(response)
#         else:
#             print("PDF를 읽지 못했어요")

# if __name__ == '__main__':
#     main()

from PyPDF2 import PdfReader
import streamlit as st
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import HuggingFaceEmbeddings

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
    documents = FAISS.from_texts(chunks, embeddings)
    return documents

def main():
    st.title("PDF 요약하기")
    st.divider()
    
    pdf = st.file_uploader('PDF파일을 업로드하세요', type='pdf')
    
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        
        if text.strip():  # 텍스트가 있는지 확인
            # PDF에서 추출한 텍스트 미리보기
            st.subheader("추출된 텍스트 미리보기")
            st.write(text[:1000])  # 처음 1000자만 보여줌
            st.divider()
            
            documents = process_text(text)
            query = "업로드된 PDF 파일의 내용을 5문장으로 요약해주세요"
            
            docs = documents.similarity_search(query)
            llm = ChatOllama(model='llama3.1:8b')
            chain = load_qa_chain(llm, chain_type='stuff')
            
            response = chain.invoke({"input_documents": docs, "question": query})
            
            st.subheader("--요약 결과--")
            st.write(response)
        else:
            st.error("PDF에서 텍스트를 추출하지 못했습니다. 다른 파일을 시도해 주세요.")
    else:
        st.info("PDF 파일을 업로드하지 않으셨습니다. 파일을 업로드해 주세요.")

if __name__ == '__main__':
    main()
