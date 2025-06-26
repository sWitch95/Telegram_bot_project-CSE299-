from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(model="mistral")

db = Chroma(
    persist_directory="embeddings/chroma",
    embedding_function=embedding_model
)

collection = db._collection
print(f"📦 Total embedded documents: {collection.count()}")
