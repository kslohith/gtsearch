import numpy as np
from fastembed import TextEmbedding

# This will trigger the model download and initialization
embedding_model = TextEmbedding()

def get_vector_embeddings(documents):
    embeddings_list = list(embedding_model.embed(documents))
    return embeddings_list