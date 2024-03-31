from fastembed import TextEmbedding
import numpy as np

def read_document(file_path):
    """Reads a text document from the given file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_embedding(text, model):
    """Generates an embedding for the given text using the specified model."""
    embedding_generator = model.embed(text)
    # Convert the generator to a NumPy array
    embedding_array = np.array(list(embedding_generator))
    return embedding_array

def cosine_similarity(vec1, vec2):
    """Computes the cosine similarity between two vectors."""
    # Access the inner vector if it's a 2-dimensional array encapsulating a single vector
    vec1 = vec1.flatten()  # Flattening the array to 1D
    vec2 = vec2.flatten()  # Flattening the array to 1D

    dot_product = np.dot(vec1, vec2)
    magnitude = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if magnitude == 0:
        return 0
    return dot_product / magnitude

# Initialize the TextEmbedding model from fastembed
model = TextEmbedding()

# Load and embed the base document and the other document
base_document_path = r'spiders\Embed\tech.txt'
other_document_path = r'spiders\Embed\docu.txt'

base_document_text = read_document(base_document_path)
other_document_text = read_document(other_document_path)

base_embedding = generate_embedding(base_document_text, model)
other_embedding = generate_embedding(other_document_text, model)

# Compute cosine similarity
similarity = cosine_similarity(base_embedding, other_embedding)
print(f'Cosine similarity: {similarity}')
