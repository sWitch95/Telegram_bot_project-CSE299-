# build_index_chunked.py
import os
import json
from tqdm import tqdm
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document

# Config
json_file = "data/modified_drug_dataset.json"
persist_directory = "embeddings/faiss"
CHUNK_SIZE = 50

# Embedding model (SentenceTransformer)
embedding_model = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2",  # চাইলে অন্য মডেল দিতে পারেন
    model_kwargs={"device": "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"}
)

# Load JSON
print("📄 Loading JSON file...")
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare all documents
all_docs = []
for entry in data:
    name = entry.get("Name", "Unknown")
    entry_type = entry.get("Type", "")
    generic_name = entry.get("Generic Name", "")

    # Include all non-empty fields
    content_parts = []
    for key, value in entry.items():
        if value and isinstance(value, str):
            content_parts.append(f"{key}: {value}")

    full_text = "\n".join(content_parts)
    all_docs.append(Document(page_content=full_text, metadata={"name": name, "type": entry_type}))

print(f"📦 Total docs to embed: {len(all_docs)}")

# Load existing FAISS index or create new
if os.path.exists(persist_directory):
    print("🔄 Loading existing FAISS index...")
    db = FAISS.load_local(
        persist_directory,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    existing_count = len(db.index_to_docstore_id)
else:
    print("🆕 Creating new FAISS index...")
    db = None
    existing_count = 0

print(f"📍 Already embedded: {existing_count} documents")

# Embed remaining chunks
for i in range(existing_count, len(all_docs), CHUNK_SIZE):
    chunk = all_docs[i:i+CHUNK_SIZE]
    print(f"🧩 Embedding docs {i} → {i+len(chunk)}")
    if db is None:
        db = FAISS.from_documents(chunk, embedding_model)
    else:
        db.add_documents(chunk)
    db.save_local(persist_directory)
    print(f"✅ Saved progress at {i+len(chunk)} docs")

print("🎉 Embedding completed successfully!")
