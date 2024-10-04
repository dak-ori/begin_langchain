from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import WikipediaRetriever

chat = ChatOpenAI()

retriever = WikipediaRetriever(
    lang='ko',
    doc_content_chars_max=500, # 최대 글자수 지정
    top_k_results=2, # 가져올 상위 검색 결과
) 

chain = RetrievalQA.from_llm(
    llm=chat, # 사용할 chat models을 설정
    retriever = retriever, # 사용할 Retriever을 설정
    return_source_documents = True, # 정보를 가져온 문서를 반환
)

result = chain("소주란?") # RetrievalQA를 실행

source_documents = result["source_documents"] # 정보 출처의 문서를 가져옴

print(f"검색 결과 : {len(source_documents)}")
for doc in source_documents:
    print("-- 검색한 메타데이터 --")
    print(doc.metadata) 
    print()
    print("-- 검색한 텍스트 --")
    print(doc.page_content[:100])
    print()
    
print("응답")
print(result["result"])