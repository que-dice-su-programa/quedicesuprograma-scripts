"""Create openai embeddings for the OpenAI documentation."""

from pdf import read_pdf
from parsers import parse

parties = ["sumar", "psoe", "pp", "vox"]
for party in parties:
    print("\nimporting " + party)

    text = read_pdf(party)
    text = parse(party, text)

    save_path = f"./data/{party}.txt"
    with open(save_path, "w") as f:
        f.write(text)

    print("\nSaved txt to " + save_path)
