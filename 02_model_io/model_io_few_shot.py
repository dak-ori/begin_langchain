from langchain.llms import OpenAI
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {
        "input" : "충청도의 계룡산 전라도의 내장산 강원도의 설악산은 모두 국립공원이다.",  # 입력 예시
        "output" : "충청도의 계룡산, 전라도의 내장산, 강원도의 설악산은 모두 국립공원이다.",  # 출력 예시
    }
]

prompt = PromptTemplate(
    input_variables=["input", "output"], # input과 output을 입력 변수로 설정
    template="입력 : {input}\n출력 : {output}", # 템플릿
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=prompt,
    prefix="아래 문장부호가 빠진 입력에 문장부호를 추가하세요. 추가할 수 있는 문장부호는 ',','.'입니다. 다른 문장부호는 추가하지 마세요.", # 지시어
    suffix="입력 : {input_string}\n출력 : ", # 출력 예시의 입력 변수 정의
    input_variables=["input_string"], # FewShotPromptTemplate를 사용해 입력 변수 설정
)
llm = OpenAI()
formatted_prompt = few_shot_prompt.format( # FewShotPromptTemplate를 사용해 프롬프트 작성
    input_string = "집을 보러 가면 그 집이 내가 원하는 조건에 맞는지 살기에 편한지 망가진 곳은 없는지 확인해야 한다"    
) 
result = llm.predict(formatted_prompt)
print("formatted_prompt: ", formatted_prompt)
print("result : ", result)
