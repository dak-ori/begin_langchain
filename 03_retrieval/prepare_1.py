from langchain.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("./sample.pdf") # pdf 파일을 로드
documents = loader.load() # 로드한 파일을 load 메서드로 정보를 저장
# load 메서드는 문장의 배열을 반환하는데, Document 라는 클래스로 표현함
# PyMuPDFLoader는 1페이지마다 1개의 Document를 생성

print(f'문서 개수: {len(documents)}') # 문서 개수를 확인
print(f'첫 번째 문서의 내용: {documents[0].page_content}') # 첫 문서의 내용을 확인
print(f'첫 번째 문서의 메타데이터: {documents[0].metadata}') # 첫 문서의 메타데이터를 확인