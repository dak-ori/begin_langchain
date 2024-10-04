from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True,
)

memory.save_context(
    {
        "input" : "안녕하세요!"
    },
    {
        "output" : "안녕하세요! 잘 지내고 계신가요? 궁금한 점이 있으면 알려주세요. 어떻게 도와드릴까요?"
    }
)

memory.save_context(
    {
        "input" : "오늘 날씨가 좋네요"
    },
    {
        "output" : "밖에 흐린데요?"
    }
)

print(memory.load_memory_variables({}))

