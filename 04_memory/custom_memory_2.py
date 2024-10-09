import chainlit as cl
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOllama
from langchain.memory import ConversationSummaryMemory

chat = ChatOllama(
    model='llama3.1:8b'
)

memory = ConversationSummaryMemory(
    llm = chat,
    return_messages=True,  
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
        
    result = chain.run(user_message)

    await cl.Message(content=result['response']).send()
    