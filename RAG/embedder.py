import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"

def create_embedding(text):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "bge-m3",
            "prompt": text
        }
    )

    embedding = response.json()["embedding"]

    return embedding