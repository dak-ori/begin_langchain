import os
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain.vectorstores import Chroma
from langchain.text_splitter import SpacyTextSplitter

embeddings = OpenAIEmbeddings(
    model = "text-embedding-ada-002"
)

chat = ChatOpenAI(model="gpt-3.5-turbo")
prompt = PromptTemplate(template="""문장을 바탕으로 질문에 답하세요.
                        
문장 : {document}
                        
질문 : {query}

""", input_variables=["document", "query"])
text_splitter = SpacyTextSplitter(chunk_size = 300, pipeline="ko_core_news_sm")

@cl.on_chat_start
async def on_chat_start():
    files = None
    
    while files is None:
        files = await cl.AskFileMessage(
            max_size_mb=20,
            content="PDF를 선택해 주세요",
            accept=["application/pdf"],
            raise_on_timeout=False,
        ).send()
    file = files[0]
    
    if not os.path.exists("tmp"): #tmp 디렉토리가 존재하는지 확인
        os.mkdir("tmp") # 없으면 디렉토리 생성
    with open(f"tmp/{file.name}", "wb") as f: # PDF를 저장 후
        f.write(file.content) # 저장한 파일 내용을 작성
        
    documents = PyMuPDFLoader(f"tmp/{file.name}").load() # 저장한 PDF 파일을 로드
    splitted_documents = text_splitter.split_documents(documents)
    
    database = Chroma(
        embedding_function=embeddings,
        # 이번에는 persist_directory 를 지정하지 않음으로써
        # 데이터베이스 영속화를 하지않음
    )
    
    database.add_documents(splitted_documents) # 문서를 데이터베이스에 저장
    
    cl.user_session.set( # 데이터베이스를 세션에 저장
        "database",  # 저장할 이름
        database     # 저장할 값
    )
    
    await cl.Message(content=f"'{file.name}' 로딩이 완료되었습니다. 질문을 입력하세요.").send()
       
@cl.on_message
async def on_message(input_message):
    print("입력된 메세지: " + input_message)
    
    database = cl.user_session.get("database")  # 세션에서 데이터베이스를 불러옴
    
    documents = database.similarity_search(input_message)
    
    documents_string = ""
    
    for document in documents:
        documents_string = f"""
        --------------------------------
        {document.page_content}
        """
        result = chat([
            HumanMessage(content=prompt.format(document=documents_string,query=input_message))
        ])
        
        await cl.Message(content=result.content).send()
                        