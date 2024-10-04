from langchain.chat_models import ChatOpenAI
from langchain.retrievers import WikipediaRetriever, RePhraseQueryRetriever
from langchain import LLMChain
from langchain.prompts import PromptTemplate
retriever = WikipediaRetriever(
    lang='ko',
    doc_content_chars_max=500
)

llm_chain = LLMChain(
    llm= ChatOpenAI(
        temperature=0, model = 'gpt-4'
    ),
    prompt= PromptTemplate(
        input_variables=["question"],
        template="""아래 질문에서 위키백과에서 검색할 키워드를 추출해주세요.
        질문: {question}
        """
    )
)

re_phrase_query_retriever = RePhraseQueryRetriever(
    llm_chain= llm_chain,
    retriever= retriever,
)

documents = re_phrase_query_retriever.get_relevant_documents("나는 라면을 좋아합니다. 그런데 소주란 무엇인가요?")

print(documents)