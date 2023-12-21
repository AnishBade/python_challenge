import os
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()
<<<<<<< HEAD
downloaded_site_path = 'downloaded_site'
# website_url = 'https://kantipurtv.com/'
# url = 'www.kantipurtv.com'  # Replace with your desired URL
website_url = 'https://ekantipur.com/'
url = 'www.ekantipur.com' 
=======
downloaded_site_path = "downloaded_site"
website_url = "https://pcampus.edu.np"
url = "pcampus.edu.np"  # Replace with your desired URL

>>>>>>> be6cde0951e1dcd29bfef6c27456cb30c6d8f8d8
depth_limit = 0  # Set your desired depth level here


# Function to download the website
def download_website():
    if not os.path.exists(downloaded_site_path):
        os.makedirs(downloaded_site_path)
<<<<<<< HEAD
        # subprocess.run(['wget', '--mirror', '--convert-links','--adjust-extension', 
        #                 '--page-requisites', '--no-parent', '--level', str(depth_limit), 
        #                 website_url, '-P', downloaded_site_path], capture_output=True, text=True)
        subprocess.run(['wget', '--mirror', '--convert-links','--adjust-extension', 
                        '--page-requisites', '--no-parent', '-l', '1', 
                        website_url, '-P', downloaded_site_path], capture_output=True, text=True)
=======
        # subprocess.run(
        #     [
        #         "wget",
        #         "--mirror",
        #         "--convert-links",
        #         "--adjust-extension",
        #         "--page-requisites",
        #         "--no-parent",
        #         "--level",
        #         str(depth_limit),
        #         website_url,
        #         "-P",
        #         downloaded_site_path,
        #     ],
        #     capture_output=True,
        #     text=True,
        # )
        subprocess.run(
            [
                "wget",
                "--mirror",
                "--convert-links",
                "--adjust-extension",
                "--page-requisites",
                "--no-parent",
                "-l",
                "2",
                website_url,
                "-P",
                downloaded_site_path,
            ],
            capture_output=True,
            text=True,
        )
>>>>>>> be6cde0951e1dcd29bfef6c27456cb30c6d8f8d8
    print("############  download_finished   ########################")


download_website()


@app.get("/")
async def read_root():
    index_path = os.path.join(downloaded_site_path, url)
    index_path = os.path.join(index_path, "index.html")

    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Index file not found.")
    return FileResponse(index_path)


@app.get("/{path:path}")
async def read_file(path: str):
    index_path = os.path.join(downloaded_site_path, url)
    full_path = os.path.join(index_path, path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(full_path)
