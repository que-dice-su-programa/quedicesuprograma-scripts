import openai
import pandas as pd
from sentence_transformers import SentenceTransformer

# calculate embeddings
LOCAL_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002" # OpenAI's best embeddings as of Apr 2023
BATCH_SIZE = 100 # you can submit up to 2048 embedding inputs per request

def create_local_embeddings(chunks):
    model = SentenceTransformer(LOCAL_EMBEDDING_MODEL)
    embeddings = model.encode(chunks)
    embeddings = map(lambda embedding: list(map(lambda y: round(y, 16), embedding)), embeddings)
    embeddings = list(embeddings)
    return pd.DataFrame({"text": chunks, "embedding": embeddings})

def create_openai_embeddings(chunks):
    embeddings = []
    for batch_start in range(0, len(chunks), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = chunks[batch_start:batch_end]
        print(f"Batch {batch_start} to {batch_end-1}")
        response = openai.Embedding.create(model=OPENAI_EMBEDDING_MODEL, input=batch)
        for i, be in enumerate(response["data"]):
            assert i == be["index"]  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)

    return pd.DataFrame({"text": chunks, "embedding": embeddings})
