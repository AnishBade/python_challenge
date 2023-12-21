import os
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from download import Downloader
app = FastAPI()

downloaded_site_path = 'downloaded_site'
parsed_url = 'annapurnapost.com'

class UrlInput(BaseModel):
    url: HttpUrl
    depth: str

@app.post("/download/")
async def process_url(url_input: UrlInput, description="Enter a website whose content is to be downloaded"):
    downloader = Downloader(url_input.url,url_input.depth )
    downloader.download_website()
    # For example, just return it back
    return {"Received URL": url_input.url, "depth_level": url_input.depth}

@app.get('/')
async def read_root():
    index_path = os.path.join(downloaded_site_path, parsed_url)
    index_path = os.path.join(index_path, 'index.html')

    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Index file not found.")
    return FileResponse(index_path)

@app.get('/{path:path}')
async def read_file(path: str):
    index_path = os.path.join(downloaded_site_path, parsed_url)
    full_path = os.path.join(index_path, path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(full_path)
