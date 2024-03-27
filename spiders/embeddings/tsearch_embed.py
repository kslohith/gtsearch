from tsearch.spiders.embeddings.tsearch_embedding_model_init import embedding_model

def get_vector_embeddings(documents):
    embeddings_list = list(embedding_model.embed(documents))
    return embeddings_list
