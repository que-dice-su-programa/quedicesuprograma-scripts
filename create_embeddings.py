"""Create openai embeddings for the Sketch documentation."""

from pdf import read_pdf
from parsers import parse_and_chunk
from embeddings import create_local_embeddings
from pprint import pprint

import nltk
nltk.download('punkt')

parties = ["podemos"]
for party in parties:
    print("\n importing " + party)

    text = read_pdf(party)
    chunks = parse_and_chunk(party, text)

    print("\nchunks: " + str(len(chunks)))
    data_frame = create_local_embeddings(chunks)
    pprint(data_frame)

    save_path = f"./data/{party}_embeddings.csv"
    data_frame.to_csv(save_path, index=False)

    print("\nSaved embeddings to " + save_path)
