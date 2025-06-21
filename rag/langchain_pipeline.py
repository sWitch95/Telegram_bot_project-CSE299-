from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama

# Step 1: LLM লোড করো (Mistral via Ollama)
llm = Ollama(model="mistral")

# Step 2: Embedding model (for Chroma vectorstore)
embedding_model = OllamaEmbeddings(model="mistral")

# Step 3: Vector store লোড করো
vectorstore = Chroma(
    persist_directory="embeddings/chroma",
    embedding_function=embedding_model,
)

# Step 4: QA Chain তৈরি করো
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=False,
)

# Step 5: Query Function
def answer_query(query: str) -> str:
    try:
        result = qa_chain.run(query)
        return result
    except Exception as e:
        return f"❌ Query Error: {str(e)}"
