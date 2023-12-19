import os
import subprocess
import logging
from flask import Flask, send_from_directory

app = Flask(__name__)
downloaded_site_path = 'downloaded_site'
website_url = 'https://www.veribom.com'  # Replace with your desired URL
depth_limit = 3  # Set your desired depth level her


logging.basicConfig(level=logging.DEBUG)

def download_website():
    if not os.path.exists(downloaded_site_path):
        os.makedirs(downloaded_site_path)
        subprocess.run(['wget', '--mirror', '--convert-links', '--adjust-extension', 
                        '--page-requisites', '--no-parent', '--level', str(depth_limit), 
                        website_url, '-P', downloaded_site_path], capture_output=True)

download_website()
 
@app.route('/')
def index():
    index_path = os.path.join(downloaded_site_path,website_url, 'index.html')
    if not os.path.exists(index_path):
        app.logger.error(f"Index file not found at {index_path}")
        return "Index file not found. Ensure the website is downloaded correctly.", 
    print("#################")
    return send_from_directory(downloaded_site_path, 'index.html')

@app.route('/<path:path>')
def serve_page(path):
    full_path = os.path.join(downloaded_site_path, path)
    print("#"*50)
    print(full_path)
    if not os.path.exists(full_path):
        app.logger.error(f"Requested path {full_path} not found")
        return "Page not found", 404
    return send_from_directory(downloaded_site_path, path)

if __name__ == "__main__":
    app.run(debug=True)
