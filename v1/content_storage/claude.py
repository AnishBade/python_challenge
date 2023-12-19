import requests
from bs4 import BeautifulSoup

base_url = 'https://www.bbc.com'

def crawl(url):
    response = requests.get(url)
    content = response.content
    page_content[url] = content
    soup = BeautifulSoup(content, 'html.parser')
    for link in soup.find_all('a'):
        path = link.get('href')
        if path and base_url in path:
            crawl(path)

page_content = {}
crawl(base_url)