# custom_web_scraper.py

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def scrape_url(url, depth, max_depth, base_domain, downloaded_site_path, visited):
    if depth > max_depth:
        return

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return
    except requests.RequestException:
        return

    # Save the current page
    parsed_url = urlparse(url)
    if base_domain not in parsed_url.netloc:
        return

    # Create appropriate local file path
    local_file_path = url.replace(f'http://{base_domain}', '').replace(f'https://{base_domain}', '')
    local_file_path = local_file_path[1:] if local_file_path.startswith('/') else local_file_path
    if local_file_path == '' or local_file_path.endswith('/'):
        local_file_path += 'index.html'  # Append 'index.html' for base domain or directory-like URLs
    elif '.' not in os.path.basename(local_file_path):
        local_file_path += '/index.html'  # Append 'index.html' for URLs that look like directories

    local_full_path = os.path.join(downloaded_site_path, local_file_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(local_full_path), exist_ok=True)
    with open(local_full_path, 'wb') as file:
        file.write(response.content)

    # Recursive call for all links on the page
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and valid_url(href):
            full_url = urljoin(url, href)
            if full_url not in visited:
                visited.add(full_url)
                scrape_url(full_url, depth + 1, max_depth, base_domain, downloaded_site_path, visited)

def custom_web_scraper(start_url, max_depth, downloaded_site_path):
    visited = set()
    base_domain = urlparse(start_url).netloc
    scrape_url(start_url, 1, max_depth, base_domain, downloaded_site_path, visited)
