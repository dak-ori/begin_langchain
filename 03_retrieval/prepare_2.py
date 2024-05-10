from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import SpacyTextSplitter 

loader = PyMuPDFLoader("./sample.pdf") # pdf 파일을 로드
documents = loader.load() # 로드한 파일을 load 메서드로 정보를 저장
# load 메서드는 문장의 배열을 반환하는데, Document 라는 클래스로 표현함
# PyMuPDFLoader는 1페이지마다 1개의 Document를 생성

text_splitter = SpacyTextSplitter( # SpacyTextSplitter 초기화
    chunk_size = 300, # 분할 크기 설정
    pipeline="ko_core_news_sm" # 분할에 사용할 언어 모델 설정
)
splitted_documents = text_splitter.split_documents(documents) # 문서 분할 

print(f'분할 전 문서 개수: {len(documents)}') # 문서 개수를 확인
print(f'분할 후 문서 개수: {len(splitted_documents)}') 
print(f'첫 번째 문서의 내용: {documents[0].page_content}') # 첫 문서의 내용을 확인
print(f'첫 번째 문서의 메타데이터: {documents[0].metadata}') # 첫 문서의 메타데이터를 확인