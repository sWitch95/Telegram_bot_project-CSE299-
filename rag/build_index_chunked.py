import os
import pandas as pd
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document

csv_folder = "data"
persist_directory = "embeddings/chroma"
CHUNK_SIZE = 1000

print("🚀 Initializing embedding model...")
embedding_model = OllamaEmbeddings(model="mistral")

print("📄 Loading CSV files...")
all_texts = []
for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        print(f"➡️ Reading: {file}")
        df = pd.read_csv(os.path.join(csv_folder, file))
        for _, row in df.iterrows():
            text = " ".join([str(v) for v in row.values if pd.notna(v)])
            all_texts.append(Document(page_content=text))

print(f"📦 Total documents to embed: {len(all_texts)}")

print("🔧 Loading existing Chroma DB...")
db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model
)
existing_count = db._collection.count()
print(f"📍 Already embedded: {existing_count} documents")

# Chunk-wise loop
for i in range(existing_count, len(all_texts), CHUNK_SIZE):
    chunk = all_texts[i:i+CHUNK_SIZE]
    print(f"\n🧩 Embedding chunk {i} → {i+len(chunk)}")
    db.add_documents(chunk)
    db.persist()
    print(f"✅ Saved up to {i+len(chunk)} documents")

print("🎉 All available documents embedded successfully!")
