
# Example list of documents
from tsearch.spiders.embeddings.tsearch_embedding_model_init import embedding_model

with open('spiders/embeddings/georgia_tech.txt', 'r') as file:
    # Read the entire content of the file
    text = file.read()
embeddings_list = list(embedding_model.embed(text))
base_embedding_tsearch = embeddings_list
