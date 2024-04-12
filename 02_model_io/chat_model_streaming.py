from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI(
    streaming = True, # 스트리밍 모드를 실행
    callbacks = [
        StreamingStdOutCallbackHandler()
        # StreamingStdOutCallbackHandler()를 callbacks로 설정
    ]
)
resp = chat ([
    HumanMessage(content="맛있는 스테이크 굽는 법을 알려주세요")
])