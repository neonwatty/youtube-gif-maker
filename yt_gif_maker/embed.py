import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def embed_chunks(chunks: list) -> np.array:
    embeddings = model.encode(chunks)
    embedding_normalizers = np.linalg.norm(embeddings, axis=1)
    normalized_embeddings = embeddings / embedding_normalizers[:, None]
    return normalized_embeddings


def embed_query(query: str):
    return model.encode([query])
