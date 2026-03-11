import sys
import os

# Add project root to Python path so 'rag' package can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import requests
from rag.retriever import search_faiss

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def build_prompt(query, retrieved_chunks):
    """
    Create prompt with context from retrieved documents
    """

    context = ""

    for chunk in retrieved_chunks:
        context += chunk["text"] + "\n"

    prompt = f"""
You are a helpful AI assistant for a gym.

Answer the user's question using ONLY the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt


def generate_answer(query):

    # Step 1: retrieve relevant chunks
    chunks = search_faiss(query)

    # Step 2: build prompt
    prompt = build_prompt(query, chunks)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json()["response"]

    else:
        raise Exception(f"LLM generation error: {response.text}")


if __name__ == "__main__":

    query = input("Ask your question: ")

    answer = generate_answer(query)

    print("\nAI Response:\n")
    print(answer)