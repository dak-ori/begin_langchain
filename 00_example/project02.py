from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import warnings

warnings.filterwarnings("ignore")

chat = ChatOpenAI(
    model = "gpt-4o",
)

input_text = input("어떤 물건을 분리수거 하시나요? : ")

prompt = PromptTemplate(
    template = "{product}는 어떻게 분리수거 하나요?",
    
    input_variables =[
        "product"
    ]
)

result = chat( # 실행
    [
        HumanMessage(content=prompt.format(product=input_text),)
    ]
)
print(result.content)