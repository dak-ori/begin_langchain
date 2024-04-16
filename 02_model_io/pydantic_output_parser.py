from langchain.output_parsers import OutputFixingParser
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, field_validator, Field # Pydantic을 불러오면서 같이 쓰는 내장함수

chat = ChatOpenAI(model="gpt-3.5-turbo")

class Smartphone(BaseModel):
    release_date : str = Field(description = "스마트폰 출시일") # 문자로 자료를 맞춘 후 Field로 추가 설명
    inch : float = Field(description = "스마트폰 크기") # 인치는 소수로 받기
    os : str = Field(description="운영체제")
    model_name : str = Field(description="모델명")
    
    field_validator("inch")
    def validate_inch(cls,field):
        if field <= 0: # inch가 0보다 작다면 
            raise ValueError("Inches must be positive number") # 반환 
        return field 
    
    
# parser = PydanticOutputParser(pydantic_object=Smartphone) # Smartphone 값으로 PydanticOutputParser 초기화
parser = OutputFixingParser.from_llm(
    parser=PydanticOutputParser(pydantic_object=Smartphone),
    llm = chat
)

result = chat([
    HumanMessage(content="안드로이드 스마트폰 하나 추천해줘"),
    HumanMessage(content=parser.get_format_instructions()) 
])

parsed_result = parser.parse(result.content)

print(f"출시일 : {parsed_result.release_date}")
print(f"크기 : {parsed_result.inch}")
print(f"OS : {parsed_result.os}")
print(f"모델명 : {parsed_result.model_name}")

