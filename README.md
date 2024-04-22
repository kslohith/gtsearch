# gtsearch

GTSearch is a search engine tailored for domain-specific inquiries related to Georgia Tech. It utilizes data obtained through a domain-specific web crawler, implemented with Scrapy as the crawling framework. Additionally, it employs a relevance engine powered by vector similarity search. We utilize Pinecone as the vector database to retrieve the top k similar documents, which are then passed as context to the OpenAI API to obtain the desired answer.


# system design

<img width="1440" alt="Screenshot 2024-04-21 at 6 28 21 PM" src="https://github.com/kslohith/gtsearch/assets/32676813/11f09439-ca89-42ab-afdf-957bad5d33fa">

System design for the crawling module

<img width="1440" alt="Screenshot 2024-04-21 at 6 28 37 PM" src="https://github.com/kslohith/gtsearch/assets/32676813/6025f4c4-f127-4761-8b65-a76a963f02bd">

System design for the RAG module

## Running Instructions

Install scrapy using pip

```shell
pip install scrapy
```
To run a crawl and insert relevant documents into pinecone

```python
scrapy crawl tsearch -o search.json
```
