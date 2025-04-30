import os
import fitz
import faiss
#import openai
from openai import OpenAI
import numpy as np
from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer

# === Config ===
PDF_FOLDER = "PDFs"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5
OPENAI_MODEL = "gpt-3.5-turbo" #"gpt-4"



# === Set your API Key ===
OpenAI.api_key = os.getenv("OPENAI_API_KEY")  # or hardcode it here (not recommended)

# === Step 1: PDF Loading ===
def extract_text_from_pdfs(folder_path):
    all_text = []
    for pdf_path in Path(folder_path).glob("*.pdf"):
        doc = fitz.open(pdf_path)
        for page in doc:
            text = page.get_text()
            if text.strip():
                all_text.append((pdf_path.name, page.number + 1, text.strip()))
    return all_text

# === Step 2: Chunking ===
def chunk_text(text: str, chunk_size=500, overlap=50) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# === Step 3: Embedding and FAISS Index ===
def create_faiss_index(chunks, model):
    texts = [chunk['text'] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

# === Step 4: Retrieval ===
def search(query, index, model, chunks, k=5):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    return [chunks[i] for i in I[0]]

# === Step 5: OpenAI LLM ===
def ask_openai(query, context_chunks):
    context = "\n\n".join(f"Source: {chunk['source']} (Page {chunk['page']})\n{chunk['text']}" for chunk in context_chunks)
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}"
    client = OpenAI(api_key=OpenAI.api_key)  # Or rely on environment variable
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# === Main CLI Flow ===
def main():
    print(f"📥 Loading PDFs from: {PDF_FOLDER}")
    raw_data = extract_text_from_pdfs(PDF_FOLDER)
    if not raw_data:
        print("No PDFs found or no extractable text.")
        return

    print(f"📄 {len(raw_data)} pages loaded. Chunking text...")
    all_chunks = []
    for fname, page_num, text in raw_data:
        for chunk in chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP):
            all_chunks.append({'text': chunk, 'source': fname, 'page': page_num})

    print(f"🧠 {len(all_chunks)} chunks created. Generating embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index, _ = create_faiss_index(all_chunks, model)

    print("✅ Ready! You can now ask questions.")
    while True:
        query = input("\n❓ Ask a question (or type 'exit' to quit): ")
        if query.lower() in {"exit", "quit"}:
            print("👋 Exiting.")
            break
        top_chunks = search(query, index, model, all_chunks, TOP_K)
        answer = ask_openai(query, top_chunks)
        print(f"\n🧾 Answer:\n{answer}\n")


main()
# if __name__ == "__main__":
#     main()
