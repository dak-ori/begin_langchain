import os
import chainlit as cl
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.schema import HumanMessage

import redis

# Upstash Redis에 연결
r = redis.Redis(
    host='ethical-snake-26354.upstash.io',
    port=6379,
    password='AWbyAAIjcDFlOTc0MzY3ZjI2MWI0NDk5ODkwZTUxZWJhNTBmMGQ5NnAxMA',
    ssl=True
)

chat = ChatOpenAI(
    model="gpt-3.5-turbo"
)

@cl.on_chat_start
async def on_chat_start():
    thread_id = None
    while not thread_id:
        res = await cl.AskUserMessage(content="채팅봇입니다, 스레드 ID를 입력하세요.", timeout=600).send()
        print(res)
        if res:
            thread_id = res['output']
            
    history = RedisChatMessageHistory(
        session_id="chat_history",
        url= os.environ.get('REDIS_URL')
    )
    
    memory = ConversationBufferMemory(
        return_messages=True,
        chat_memory=history,
    )
    
    chain = ConversationChain(
        memory=memory,
        llm=chat,
    )
    
    memory_message_result = chain.memory.load_memory_variables({})
    
    messages = memory_message_result['history']
    
    for message in messages:
        if isinstance(message,HumanMessage):
            await cl.Message(
                author='User',
                content=f"{message.content}",
            ).send()
        else:
            await cl.Message(
                author="ChatBot",
                content=f"{message.content}"
            ).send()
    cl.user_session.set("chain", chain)



@cl.on_message
async def on_message(message:str):
    chain = cl.user_session.get("chain")
    user_message = message.content if hasattr(message, 'content') else str(message)
    result = chain.run(user_message)
    await cl.Message(content=result["response"]).send()

