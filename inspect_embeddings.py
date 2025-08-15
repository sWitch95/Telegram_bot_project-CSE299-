from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(model="mistral")

db = Chroma(
    persist_directory="embeddings/chroma",
    embedding_function=embedding_modelfrom langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

# Load same embedding model you used for building index
embedding_model = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

persist_directory = "embeddings/faiss"

if os.path.exists(persist_directory):
    db = FAISS.load_local(
        persist_directory,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    print(f"📦 Total embedded documents: {len(db.docstore._dict)}")
else:
    print("❌ FAISS index not found.")

)

collection = db._collection
print(f"📦 Total embedded documents: {collection.count()}")
