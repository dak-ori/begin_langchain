from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI( # 클라이언트 생성 및 chat에 저장
    model = "gpt-3.5-turbo", # 호출 할 모델
)

# 1. input_variables 를 이용한 초기화 방법
prompt = PromptTemplate( # PromptTemplate 작성
    template = "{product}는 어느 회사에서 개발한 제품인가요?", # {product}라는 포함하는 프롬프트 작성
    
    input_variables =[
        "product" # product에 입력할 변수 지정
    ]
)
# 2. PromptTemplate 를 바로 초기화
# prompt = PromptTemplate.from_template("{product}는 어느 회사에서 개발한 제품인가요?") 

result = chat( # 실행
    [
        HumanMessage(content=prompt.format(product="아이폰"),) # prompt.format 실행해 프롬프트 생성
    ]
)
print(result.content) # 결과를 표시