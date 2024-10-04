import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage

chat = ChatOpenAI(
    model = "gpt-4"
)

memory = ConversationBufferMemory(
    return_messages=True,
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="메세지를 입력하세요.").send()
    
@cl.on_message
async def on_message(message : str):
    memory_message_result = memory.load_memory_variables({}) # 메모리 내용을 로드
    
    messages = memory_message_result['history'] # 메모리에서 메시지만 받음
    
    messages.append(HumanMessage(content=message)) # 사용자의 메시지를 추가
    
    result = chat( # 언어모델을 호출
        messages
    )
    
    memory.save_context( # 사용자의 메시지와 AI의 메시지를 메모리에 저장
        {
            "input" : message, # 사용자의 메시지는 input
        },
        {
            "output" : result.content, # AI의 메세지는 output
        }
    )
    await cl.Message(content=result.content).send()