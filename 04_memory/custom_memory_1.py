import chainlit as cl
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory

chat = ChatOpenAI(
    model= 'gpt-3.5-turbo'
)

memory = ConversationBufferWindowMemory(
    return_messages=True,
    k = 3  
    ## 3번까지 주고받은 메시지를 기억 -> 4번째 부터 메세지를 삭제 시작
    ## 보내는 메세지, 받는 메세지 2개가 1쌍이므로 총 6개까지 저장 가능
)

chain = ConversationChain(
    memory=memory,
    llm=chat,
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="채팅봇입니다. 메세지를 입력하세요.").send()

@cl.on_message
async def on_message(message: str):
    user_message = message.content if hasattr(message, 'content') else str(message)
    messages = chain.memory.load_memory_variables({})['history']
    print(f"저장된 메세지 개수 : {len(messages)}")
    
    for saved_message in messages:
        print(saved_message.content)
        
    result = chain(user_message)

    await cl.Message(content=result['response']).send()
    