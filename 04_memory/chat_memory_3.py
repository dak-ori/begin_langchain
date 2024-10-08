import os
import chainlit as cl
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory import RedisChatMessageHistory
from langchain.chains import ConversationChain
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

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="메세지를 입력하세요.").send()

@cl.on_message
async def on_message(message):
    # message 객체에서 텍스트(content)를 추출하여 사용
    user_message = message.content if hasattr(message, 'content') else str(message)
    
    # 대화 처리
    result = chain.run(user_message)
    
    # 사용자가 입력한 메시지를 Redis에 저장
    r.set("last_user_message", user_message)  # 예시: 마지막 사용자 메시지를 저장

    await cl.Message(content=result).send()
