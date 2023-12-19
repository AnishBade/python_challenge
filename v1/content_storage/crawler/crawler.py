import requests
from bs4 import BeautifulSoup

pages = {} 

def crawl(url):
    response = requests.get(url)
    pages[url] = response.content

    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        path = link.get('href')
        if path.startswith('/'):  
            crawl(url + path)
            
def get_pages():
    return pages