import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain import hub
import glob

VECTOR_STORE_PATH = r"C:\github\RAG\vectorstore"
EMBEDDINGS = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")


# Create a vectorstore from a list of PDFs
def create_vectorstore():
    list_of_pdfs = glob.glob("C:/Users/U701/바탕 화면/강서운이야기/데이터/데이터/*.pdf")
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    documents = []
    for pdf in list_of_pdfs:
        loader = PyPDFLoader(pdf)
        documents += loader.load()

    chunked_documents = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunked_documents, EMBEDDINGS)
    vectorstore.save_local(VECTOR_STORE_PATH)

    return vectorstore


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    # Check if the vector store exists
    if not os.path.exists(VECTOR_STORE_PATH):
        print("벡터 저장소가 존재하지 않습니다. 생성 중...")
        vectorstore = create_vectorstore()
    else:
        print("벡터 저장소를 로드하는 중...")
        try:
            vectorstore = FAISS.load_local(
                VECTOR_STORE_PATH, EMBEDDINGS, allow_dangerous_deserialization=True
            )
        except RuntimeError as e:
            print(f"벡터 저장소 로드 중 오류 발생: {e}")
            return

    # Load the prompt
    prompt = hub.pull("rlm/rag-prompt")

    # Initialize the model
    llm = ChatOllama(model="gemma:7b")

    # Create chain with source
    retriever = vectorstore.as_retriever()
    rag_chain_from_docs = (
        RunnablePassthrough.assign(
            context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )
    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    # Query
    query = "2022년부터 2024년까지 한국은행의 통화정책 주요 목표는 무엇이었나요?"
    response = rag_chain_with_source.invoke(query)

    # Print response
    print("Answer:\n", response["answer"] + "\n")
    print("Sources:")
    sources = [doc.metadata for doc in response["context"]]
    for source in sources:
        print(source)


if __name__ == "__main__":
    main()
    
    """VECTOR_STORE_PATH = "./vectorstore"
EMBEDDINGS = HuggingFaceEmbeddings(model_name = "intfloat/multilingual-e5-small")

def create_vectorstore():
    list_of_pdfs = glob.glob("C:/Users/U701/Desktop/강미네이터/데이터/*.pdf") # 이 경로에 있는 모든 pdf파일의 주소를 list 형식으로 저장
    list_of_pdfs = glob.glob("C:/Users/U701/Desktop/강서운이야기/데이터/데이터/*.pdf") # 이 경로에 있는 모든 pdf파일의 주소를 list 형식으로 저장
    text_splitter = CharacterTextSplitter( # CharacterTextSplitter 객체 생성
        separator='\n', # 줄바꿈을 기준으로 분할
        chunk_size = 1000, # 분할된 텍스트의 크기는 1000자
@ -55,7 +55,7 @@ def main():
    
    prompt = hub.pull("rlm/rag-prompt") # 질의응답에 사용할 프롬프트
    
    llm = ChatOllama(model="llama3.1:8b") # 사용할 모델
    llm = ChatOllama(model="gemma:7b") # 사용할 모델
    
    retriever = vectorstore.as_retriever() # 벡터 저장소를 검색기로 변환
    rag_chain_from_docs = ( 
@ -69,7 +69,7 @@ def main():
        {"context" : retriever, "question" : RunnablePassthrough()} # 검색기는 context를 제공, 사용자의 질문은 직접 처리
    ).assign(answer = rag_chain_from_docs) # rag_chain_from_docs에서 생성된 답변을 결과로 지정
    
    query = "모든 PDF 내용을 요약해서 서술해줘"
    query = "2022년부터 2024년까지 한국은행의 통화정책 주요 목표는 무엇이었나요?"
    response = rag_chain_with_source.invoke(query) # 체인을 사용하여 질의를 실행 수 결과를 저장
    
    print("Answer:\n", response["answer"] + "\n") # 답변 출력

    """