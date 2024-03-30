from fastembed import TextEmbedding
import numpy as np
from pathlib import Path
from collections import deque
import scrapy
from urllib.parse import urlparse

def extract_hostname(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

url_seen = set()
urls_frontier = deque()

class TechSpider(scrapy.Spider):
    name = "tsearch"

    def start_requests(self):
        urls = [
            "https://www.cc.gatech.edu/",
            "https://library.gatech.edu/",
            "https://pe.gatech.edu/degrees/computer-science",
            "https://www.reddit.com/r/OMSCS/",
            "https://www.reddit.com/r/gatech/",
            "https://www.omscentral.com/",
            "https://spp.gatech.edu/spp_newsletters",
            "https://scs.gatech.edu/news",
            "https://db.cc.gatech.edu/",
            "https://coe.gatech.edu/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
            text_content = ""
            p_tag_content = response.xpath('//p')
            for p_tag in p_tag_content:
                p_text = p_tag.xpath('string()').get().strip()
                text_content += p_text
                yield{
                     "paragraph": p_text
                }
            #print(text_content)
            print(get_similarity_scores(text_content))

def read_document(file_path):
    """Reads a text document from the given file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_embedding(text, model):
    """Generates an embedding for the given text using the specified model."""
    # Assuming model.embed returns a suitable array-like structure directly
    return np.array(model.embed(text))

def cosine_similarity(vec1, vec2):
    """Computes the cosine similarity between two vectors."""
    vec1 = vec1.flatten()
    vec2 = vec2.flatten()
    dot_product = np.dot(vec1, vec2)
    magnitude = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    if magnitude == 0:
        return 0
    return dot_product / magnitude

def get_similarity_scores(text_content):
    model = TextEmbedding()

    base_document_path = r'spiders\Embed\tech.txt'
    base_document_text = read_document(base_document_path)
    base_embedding = generate_embedding(base_document_text, model)
    
    other_embedding = generate_embedding(text_content, model)

    return cosine_similarity(base_embedding, other_embedding)
