from langchain.retrievers import WikipediaRetriever
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


retrievers = WikipediaRetriever( 
    lang='ko', # 위키백과의 언어 지정
)

documents = retrievers.get_relevant_documents(
    "대형 언어 모델" # 검색할 키워드를 지정
)

print(f"검색결과 : {len(documents)}건")

for document in documents:
    print("\n-- 검색한 메타데이터 --")
    print(document.metadata) 
    print("\n-- 검색한 텍스트 --")
    print(document.page_content[:100]) # 기사내용을 저장