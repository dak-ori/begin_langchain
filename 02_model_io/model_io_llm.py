from langchain.llms import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-instruct") # 모델 호출

result = llm(
    "맛있는 라면을", # 모델에 입력되는 메세지
    stop = "." # 출력중 .을 출력한다면 정지
)

print(result)