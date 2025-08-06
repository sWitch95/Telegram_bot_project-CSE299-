import os
import json
from tqdm import tqdm
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document

json_file = "data/modified_drug_dataset.json"
persist_directory = "embeddings/chroma"
CHUNK_SIZE = 50

print("🚀 Initializing embedding model...")
embedding_model = OllamaEmbeddings(model="mistral")

print("📄 Loading JSON file...")
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

all_texts = []
print("🧾 Preparing documents for embedding...")
for i, entry in enumerate(data):
    name = entry.get("Name", "Unknown")
    entry_type = entry.get("Type", "Generic")
    generic_name = entry.get("Generic Name", "")
    aliases = [name]
    if generic_name and generic_name.lower() not in name.lower():
        aliases.append(generic_name)
    alias_str = ", ".join(aliases)

    # Log the drug being embedded
    print(f"➡️ Embedding: {name} ({entry_type})")

    # Make brand/generic names prominent
    text = (
        f"Brand Name: {name}\n"
        f"Type: {entry_type}\n"
        f"Generic Name: {generic_name}\n"
        f"Aliases: {alias_str}\n"
        + " ".join([str(v) for v in entry.values() if v])
    )
    all_texts.append(Document(page_content=text))

print(f"\n📦 Total documents to embed: {len(all_texts)}")

print("🔧 Loading existing Chroma DB...")
db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model
)
existing_count = db._collection.count()
print(f"📍 Already embedded: {existing_count} documents")

# Chunk-wise embedding loop
for i in range(existing_count, len(all_texts), CHUNK_SIZE):
    chunk = all_texts[i:i+CHUNK_SIZE]
    print(f"\n🧩 Embedding chunk {i} → {i+len(chunk)}")
    db.add_documents(chunk)
    db.persist()
    print(f"✅ Saved up to {i+len(chunk)} documents")

print("🎉 All available documents embedded successfully!")