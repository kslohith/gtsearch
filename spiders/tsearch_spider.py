from pathlib import Path
from collections import deque
import scrapy
from urllib.parse import urlparse
from tsearch.spiders.embeddings.similarity_search_embeddings import get_similarity_scores

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
            print(text_content)
            print(get_similarity_scores(text_content))
            # TODO: Add vector embedding filter
            # here is where we will add our implementation of vector search to decide whether to crawl this page or not
            links = response.xpath('//a')
            # Loop through each link and extract the href attribute
            for link in links:
                href = link.xpath('@href').extract_first()
                if href is not None and ("https" not in href and "http" not in href):
                     href = "https://" + str(extract_hostname(response.url)) + href
                if href not in url_seen:
                     url_seen.add(href)
                     urls_frontier.append(href)
            #Get a Valid url from url frontier
            while len(urls_frontier) > 0 and urls_frontier[0] is None:
                 urls_frontier.popleft()
            try:
                print("*****Exploring url******", urls_frontier[0], len(url_seen))
                yield scrapy.Request(url=urls_frontier.popleft(), callback=self.parse, dont_filter=True)
            except:
                pass
            

            
            
            