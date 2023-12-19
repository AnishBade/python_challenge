# app.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from custom_web_scraper import custom_web_scraper
import os
from urllib.parse import urlparse

app = FastAPI()
downloaded_site_path = 'downloaded_site'
website_url = 'https://www.veribom.com'  # Replace with your desired URL
depth_limit = 3  # Set your desired depth level here

# Start the scraping process
custom_web_scraper(website_url, depth_limit, downloaded_site_path)

@app.get('/{path:path}')
async def serve_page(path: str):
    base_domain = urlparse(website_url).netloc
    local_file_path = path.replace(base_domain, '').replace('http://', '').replace('https://', '')
    local_full_path = os.path.join(downloaded_site_path, local_file_path)

    # Handle directory paths - look for an index.html file in the directory
    if os.path.isdir(local_full_path):
        index_file_path = os.path.join(local_full_path, 'index.html')
        if os.path.exists(index_file_path):
            return FileResponse(index_file_path)
        else:
            raise HTTPException(status_code=404, detail="Directory index file not found")

    if not os.path.exists(local_full_path):
        raise HTTPException(status_code=404, detail="Page not found or beyond depth limit")
    return FileResponse(local_full_path)
