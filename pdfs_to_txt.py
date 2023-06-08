"""Create openai embeddings for the Sketch documentation."""

from pdf import read_pdf

parties = ["podemos", "psoe", "pp", "vox"]
parties = ["podemos"]
for party in parties:
    print("\nimporting " + party)

    text = read_pdf(party)

    save_path = f"./data/{party}.txt"
    with open(save_path, "w") as f:
        f.write(text)

    print("\nSaved txt to " + save_path)
