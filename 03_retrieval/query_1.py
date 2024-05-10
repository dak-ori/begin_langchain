from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002"
)

database = Chroma(
    persist_directory="./.data",
    embedding_function = embeddings
)

documents = database.similarity_search("비행 자동차의 최고속도는?")
print(f'문서 개수: {len(documents)}')

for document in documents:
    print(f'문서 내용: {document.page_content}')