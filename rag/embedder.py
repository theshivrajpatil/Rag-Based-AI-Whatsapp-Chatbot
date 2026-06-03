from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

model = load_model()

def get_embeddings(texts):
    return model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False
    ).tolist()