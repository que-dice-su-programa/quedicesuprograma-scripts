# Programas scripts

This script crates embeddings for the PDF programs of spanish parties.

## Installation

You'll need python 3.9.6 and pip installed.

```
make setup
```

## Creating embeddings

You'll need to run

```
python ./create_embeddings.py
```

The embeddings file will be outputted to `./data/{party}_embeddings.csv`
