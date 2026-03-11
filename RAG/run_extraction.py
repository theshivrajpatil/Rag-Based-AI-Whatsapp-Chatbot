import sys
import os

# Add project root to Python path so 'rag' package can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from rag.text_extractor import extract_all_pdfs

input_folder = "data/gym_docs"
output_folder = "data/raw_text"

extract_all_pdfs(input_folder, output_folder)

print("Text extraction completed")