import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="study_materials"
)

def store_chunks(
    chunks,
    embeddings,
    file_hash,
    file_name
):

    ids = [
        f"{file_hash}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "file_hash": file_hash,
            "file_name": file_name
        }
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


def document_exists(file_hash):

    results = collection.get(
        where={
            "file_hash": file_hash
        }
    )

    return len(results["ids"]) > 0


def retrieve(query_embedding, k=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )

    documents = results["documents"][0]

    sources = [
        metadata.get("file_name", "Unknown")
        for metadata in results["metadatas"][0]
        if metadata
    ]

    return documents, sources