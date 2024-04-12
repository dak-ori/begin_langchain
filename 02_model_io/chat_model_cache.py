import time
from turtle import st 
import langchain

from langchain.cache import InMemoryCache
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

langchain.llm_cache = InMemoryCache() # InMemoryCache는 일시적으로 데이터를 보관하는 캐쉬를 제공하는 클래스 
chat = ChatOpenAI()
start = time.time() # 실행 시작시간을 start에 기록
result = chat ([
    HumanMessage(content="안녕하세요!")
])

end = time.time() # 실행 종료시간을 end에 기록
print(result.content) # result 출력
print(f"실행시간 : {end - start}초")

chat = ChatOpenAI()
start = time.time() # 실행 시작시간을 start에 기록
result = chat ([ # 캐쉬를 활용하여 즉시 실행 완료
    HumanMessage(content="안녕하세요!")
])

end = time.time() # 실행 종료시간을 end에 기록
print(result.content) # result 출력
print(f"실행시간 : {end - start}초")


