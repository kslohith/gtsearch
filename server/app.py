from flask import Flask, jsonify, request
import numpy as np
from pinecone import Pinecone, ServerlessSpec
from embedding import get_vector_embeddings
from openai import OpenAI
from flask_cors import CORS
import os

os.environ['OPENAI_API_KEY'] = os.environ.get('openai_secret')

app = Flask(__name__)
CORS(app)
pc = Pinecone(api_key=os.environ.get('pinecone_secret'))
index = pc.Index("tsearch")

# Route to add a new book
@app.route('/tsearch/search', methods=['POST'])
def ask_tsearch():
    search_query = request.json
    search_embedding = np.array(get_vector_embeddings(search_query["search_query"]))
    results = index.query(vector=search_embedding.tolist()[0], top_k=5, include_metadata=True, namespace='ns1')
    context = ""
    link = []
    result_array = results.get('matches')
    for res in result_array:
        metadata = res.get('metadata')
        context += metadata.get('text')
        link.append(metadata.get('url'))

    context.replace("\n", "")

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    query_message = f"using this as context {context} answer the following question {search_query['search_query']}, also use the below list of urls to give out any of these urls if it relevant to the question {link}. All questions are based on georgia tech."
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query_message,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
