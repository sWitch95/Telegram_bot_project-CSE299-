import os
import pandas as pd
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document

csv_folder = "data"
persist_directory = "embeddings/chroma"

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

print(f"✅ Total documents loaded: {len(all_texts)}")

# ✅ Only process 100 docs first (for debugging)
sample_docs = all_texts[:100]

print("🔧 Creating vectorstore (100 sample docs)...")
vectorstore = Chroma.from_documents(
    documents=tqdm(sample_docs, desc="🔄 Embedding docs"),
    embedding=embedding_model,
    persist_directory=persist_directory,
)

print("💾 Saving vector DB...")
vectorstore.persist()
print("✅ Done!")
