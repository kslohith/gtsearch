from tsearch.spiders.embeddings.tsearch_base_embedding import base_embedding_tsearch
from tsearch.spiders.embeddings.tsearch_embed import get_vector_embeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
index = pc.Index("tsearch")

def insert_vectors_to_pinecone(document, url, id):
    embedding = np.array(get_vector_embeddings(document))
    vectors = []
    data_dict = {}
    metadata_dict = {}
    metadata_dict["text"] = document
    metadata_dict["url"] = url
    data_dict["id"] = str(id)
    data_dict["values"] = embedding.tolist()[0]
    data_dict["metadata"] = metadata_dict
    vectors.append(data_dict)
    print(vectors)
    try:
        index.upsert(vectors,namespace= "ns1")
    except Exception as e:
        print(e)

def get_similarity_scores(documents, current_url, document_number):
    insert_vectors_to_pinecone(document=documents, url=current_url, id=document_number)
    current_vector_embedding = np.array(get_vector_embeddings(documents))
    base_embedding = np.array(base_embedding_tsearch)
    current_vector_embedding = current_vector_embedding.reshape(1, -1)
    base_embedding = base_embedding.reshape(1, -1)
    similarity = cosine_similarity(current_vector_embedding, base_embedding)

    return similarity[0][0]



