import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage

from langchain.chains import ConversationChain

chat = ChatOpenAI(
    model = "gpt-4"
)

memory = ConversationBufferMemory(
    return_messages=True,
)

chain = ConversationChain(
    memory= memory,
    llm=chat,
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="메세지를 입력하세요.").send()
    
@cl.on_message
async def on_message(message : str):

    result = chain(
        message
    )
    
    await cl.Message(content=result["response"]).send()