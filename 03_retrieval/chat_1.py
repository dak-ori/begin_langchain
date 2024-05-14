import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="준비되었습니다! 메세지를 입력하세요!").send() # 시작 메세지 표기

@cl.on_message
async def on_message(input_message):
    print("입력된 메세지: " + input_message)
    await cl.Message(content="안녕하세요!").send() # 챗봇의 답변을 보냄