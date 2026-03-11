import faiss
import numpy as np
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "bge-m3"


def get_query_embedding(query):

    payload = {
        "model": MODEL_NAME,
        "prompt": query
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return np.array(response.json()["embedding"]).astype("float32")

    else:
        raise Exception(f"Embedding error: {response.text}")


def search_faiss(query, top_k=3):

    # Load index
    index = faiss.read_index("vector_db/faiss_index.bin")

    # Load metadata
    with open("vector_db/metadata.json", "r") as f:
        metadata = json.load(f)

    # Convert query to embedding
    query_vector = get_query_embedding(query)

    query_vector = np.array([query_vector]).astype("float32")

    # Search
    distances, indices = index.search(query_vector, top_k)

    results = []

    for idx in indices[0]:
        results.append(metadata[idx])

    return results


if __name__ == "__main__":

    query = input("Ask your question: ")

    results = search_faiss(query)

    print("\nTop Results:\n")

    for r in results:
        print(r["text"])
        print("------")