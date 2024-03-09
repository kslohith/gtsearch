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
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
            p_tag_content = response.xpath('//p')
            for p_tag in p_tag_content:
                p_text = p_tag.xpath('string()').get().strip()
                yield{
                     "paragraph": p_text
                }
            h_tag_content = response.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6')
            for heading_tag in h_tag_content:
                heading_text = heading_tag.xpath('string()').get().strip()
                yield{
                     "header": heading_text
                }
            # TODO: Add vector embedding filter
            # here is where we will add our implementation of vector search to decide whether to crawl this page or not
            links = response.xpath('//a')
            # Loop through each link and extract the href attribute
            for link in links:
                href = link.xpath('@href').extract_first()
                if href is not None and "https" not in str(href):
                     href = str(extract_hostname(response.url)) + href
                if href not in url_seen:
                     url_seen.add(href)
                     urls_frontier.append(href)
            

            
            
            