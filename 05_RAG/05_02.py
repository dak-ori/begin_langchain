from langchain_community.document_loaders import TextLoader
documents = TextLoader("C:/github/begin_langchain/05_RAG/AI.txt").load()

from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs

docs = split_docs(documents)

from langchain_huggingface import HuggingFaceEmbeddings
EMBEDDINGS = HuggingFaceEmbeddings(model_name = "intfloat/multilingual-e5-small") 

from langchain_community.vectorstores import FAISS
db = FAISS.from_documents(docs, EMBEDDINGS)

from langchain_community.chat_models import ChatOllama
llm = ChatOllama(model="llama3.1:8b")

from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm, chain_type="stuff", verbose=True)

query = "AI가 무엇인지 한글로 설명해줘"
matching_docs = db.similarity_search(query)
answer = chain.invoke({"input_documents" : matching_docs, "question" : query})
print(answer)