import os
from deep_translator import GoogleTranslator
from langdetect import detect
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_community.embeddings import SentenceTransformerEmbeddings
from dotenv import load_dotenv

# Load env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🧠 Embedding model (SentenceTransformer)
embedding_model = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2",  # বা অন্য মডেল
    model_kwargs={"device": "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"}
)

# 🧠 LLM model (Groq llama-3.1-8b-instant)
llm_model = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)

# Load FAISS vectorstore
persist_directory = "embeddings/faiss"
if os.path.exists(persist_directory):
    vectorstore = FAISS.load_local(
        persist_directory,
        embedding_model,
        allow_dangerous_deserialization=True
    )
else:
    vectorstore = None

retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) if vectorstore else None
qa_chain = RetrievalQA.from_chain_type(llm=llm_model, retriever=retriever) if retriever else None

# 🌐 Translate helper
def translate(text: str, source: str, target: str) -> str:
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except:
        return text

# 🎯 Main function
def answer_query(query: str) -> str:
    lang = detect(query)
    if lang not in ['en', 'bn']:
        lang = 'en'
    
    query_en = translate(query, source='auto', target='en')
    
    if qa_chain is None:
        return "❌ FAISS index not loaded. Please build index first."
    
    result = qa_chain.invoke({"query": query_en})
    answer_en = result.get("result", "").strip()
    
    if not answer_en:
        return "দুঃখিত, আমি আপনার প্রশ্নের উত্তর খুঁজে পাইনি।" if lang == "bn" else "Sorry, I couldn't find the answer."
    
    if lang == "bn":
        return translate(answer_en, source='en', target='bn')
    else:
        return answer_en

# ✅ Test mode
if __name__ == "__main__":
    query = "What is Paracetamol?"
    if vectorstore:
        docs = vectorstore.similarity_search(query, k=5)
        for i, doc in enumerate(docs):
            print(f"Result {i+1}:\n{doc.page_content}\n{'-'*40}")
    else:
        print("❌ FAISS index not loaded.")
