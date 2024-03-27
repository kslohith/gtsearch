from tsearch.spiders.embeddings.tsearch_base_embedding import base_embedding_tsearch
from tsearch.spiders.embeddings.tsearch_embed import get_vector_embeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity_scores(documents):
    current_vector_embedding = np.array(get_vector_embeddings(documents))
    base_embedding = np.array(base_embedding_tsearch)

    current_vector_embedding = current_vector_embedding.reshape(1, -1)
    base_embedding = base_embedding.reshape(1, -1)

    similarity = cosine_similarity(current_vector_embedding, base_embedding)

    print(similarity[0][0])

    return similarity[0][0]



