from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate

quest = input("무엇을 알려드릴까요? > ")
chat = ChatOpenAI(
    model = "gpt-3.5-turbo",
    streaming = True,
    callbacks = [
        StreamingStdOutCallbackHandler() # 출력을 지원함
    ])

prompt = PromptTemplate(
    template = "{product}는 무엇인가요?",
    input_variables = ["quest"]
)
result = chat(
    [
        HumanMessage(content=prompt.format(product=quest))
        
    ]
)
