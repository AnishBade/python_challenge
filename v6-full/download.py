from logger import logger
import subprocess
import os
from urllib.parse import urlparse
downloaded_site_path = 'downloaded_site'
class Downloader():
    def __init__(self,url, depth_level) -> None:
        self.url = url
        self.depth_level = depth_level
        self.parsed_url = urlparse(url)

        

    def download_website(self):
        logger.info(
            f"Started downloading website contents of  {self.url}."
        )
        if not os.path.exists(downloaded_site_path):
            os.makedirs(downloaded_site_path)
        print(type(str(self.parsed_url)))
        # print(os.path.join(downloaded_site_path, strself.parsed_url)
        if not os.path.exists(os.path.join(downloaded_site_path, str(self.parsed_url))):

            subprocess.run(['wget', '--mirror', '--convert-links','--adjust-extension', 
                            '--page-requisites', '--no-parent', '-l', self.depth_level, 
                        self.url, '-P', downloaded_site_path], capture_output=True, text=True)
        print("############  download_finished   ########################")

    
