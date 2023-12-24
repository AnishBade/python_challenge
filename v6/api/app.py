import os
from urllib.parse import urlparse

from download import Downloader
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from logger import configure_logging
from loguru import logger
from pydantic import BaseModel, HttpUrl

app = FastAPI()

downloaded_site_path = "downloaded_site"
parsed_url = "www.veribom.com"
configure_logging()


class UrlInput(BaseModel):
    url: HttpUrl
    depth: str


@app.post("/download/")
async def process_url(
    url_input: UrlInput, description="Enter a website whose content is to be downloaded"
):
    try:
        downloader = Downloader(url_input.url, url_input.depth)

        await downloader.download_website()
        logger.success(f"Download Succesfulfor {str(url_input.url)}")
        return JSONResponse(
            content={"Received url": str(url_input.url), "depth_level": url_input.depth}
        )
        # return {"Received URL": url_input.url, "depth_level": url_input.depth}
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": "Download Failed"}, status_code=500)


@app.get("/")
async def read_root():
    try:
        index_path = os.path.join(downloaded_site_path, parsed_url)
        index_path = os.path.join(index_path, "index.html")

        if not os.path.exists(index_path):
            raise HTTPException(status_code=404, detail="Index file not found.")
        return FileResponse(index_path)
    except HTTPException as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": e.detail}, status_code=500)
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": "Something Went Wrong"}, status_code=500)


@app.get("/{path:path}")
async def read_file(path: str):
    try:
        index_path = os.path.join(downloaded_site_path, parsed_url)
        full_path = os.path.join(index_path, path)
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="Page not found")
        return FileResponse(full_path)
    except HTTPException as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": e.detail}, status_code=500)
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": "Something Went Wrong"}, status_code=500)
