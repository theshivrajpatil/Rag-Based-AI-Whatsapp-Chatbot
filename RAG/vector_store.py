import faiss
import numpy as np
import json
import os


def build_faiss_index(embeddings_file, metadata_file, output_folder):

    embeddings = np.load(embeddings_file)

    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print(f"Total vectors indexed: {index.ntotal}")

    os.makedirs(output_folder, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, os.path.join(output_folder, "faiss_index.bin"))

    # Copy metadata
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    with open(os.path.join(output_folder, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print("FAISS index saved successfully")


if __name__ == "__main__":

    embeddings_file = "vector_db/embeddings.npy"
    metadata_file = "vector_db/metadata.json"
    output_folder = "vector_db"

    build_faiss_index(embeddings_file, metadata_file, output_folder)