import pandas as pd
from sentence_transformers import SentenceTransformer

# calculate embeddings
LOCAL_EMBEDDING_MODEL = "hiiamsid/sentence_similarity_spanish_es"

def create_local_embeddings(chunks):
    model = SentenceTransformer(LOCAL_EMBEDDING_MODEL)
    embeddings = model.encode(chunks)
    embeddings = map(lambda embedding: list(map(lambda y: round(y, 16), embedding)), embeddings)
    embeddings = list(embeddings)
    return pd.DataFrame({"text": chunks, "embedding": embeddings})
