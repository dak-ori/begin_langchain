from langchain.embeddings import OpenAIEmbeddings
from numpy import dot
from numpy.linalg import norm

embeddings = OpenAIEmbeddings(
    model = "text-embedding-ada-002"
    #ada-002는 텍스트를 벡터화하면 1536차원의 벡터를 출력한다.
)

# 벡터화하기
query_vector = embeddings.embed_query("비행 자동차의 최고 속도는?")  # 질문을 벡터화
print(f'벡터화된 질문: {query_vector[:5]}') # 벡터의 일부를 표시

# 벡터 유사도 계산하기
document_1_vector = embeddings.embed_query("비행 자동차의 최고 속도는 시속 150km 입니다.") # 문서 1의 벡터를 얻음
document_2_vector = embeddings.embed_query("닭고기를 적당히 양념한 후 중불로 굽다가 가끔 뒤집어 주면서 겉은 고소하고 속은 부드럽게 익힌다.") # 문서 2의 벡터를 얻음

# ada는 코사인 유사도를 사용해 유사도를 계산하는 것을 권장
cos_sim_1 = dot(query_vector, document_1_vector) / (norm(query_vector)) * norm(document_1_vector)
print(f'문서 1과 질문의 유사도: {cos_sim_1}')
cos_sim_2 = dot(query_vector, document_2_vector) / (norm(query_vector)) * norm(document_2_vector)
print(f'문서 2와 질문의 유사도: {cos_sim_2}')