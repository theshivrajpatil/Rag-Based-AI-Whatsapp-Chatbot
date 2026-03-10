import os
import json


def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into chunks with overlap.
    chunk_size = number of words per chunk
    overlap = overlapping words between chunks
    """

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):

        end = start + chunk_size
        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def process_text_files(input_folder, output_file):
    """
    Read all extracted text files and create chunks
    """

    all_chunks = []

    for file in os.listdir(input_folder):

        if file.endswith(".txt"):

            file_path = os.path.join(input_folder, file)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)

            for chunk in chunks:
                all_chunks.append({
                    "source": file,
                    "text": chunk
                })

            print(f"Chunked {file}")

    # save chunks
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print("All chunks saved successfully")


if __name__ == "__main__":

    input_folder = "data/raw_text"
    output_file = "data/processed/chunks.json"

    os.makedirs("data/processed", exist_ok=True)

    process_text_files(input_folder, output_file)