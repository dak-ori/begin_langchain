from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import DatetimeOutputParser
from langchain.schema import HumanMessage
from langchain.output_parsers import OutputFixingParser

output_parser = DatetimeOutputParser()


chat = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate.from_template("{product}의 출시일을 알려주세요")


result = chat(
    [
        HumanMessage(content=prompt.format(product="아이폰"),),
        HumanMessage(content=output_parser.get_format_instructions()), # 오류가 나는 원인
    ]
)

output = output_parser.parse(result.content)

print(output)