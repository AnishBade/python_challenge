import os
import subprocess
from urllib.parse import urlparse

from logger import configure_logging, logger
from utils.logger import PythonLoggerExtension

downloaded_site_path = "downloaded_site"
python_exception = PythonLoggerExtension()
configure_logging()


class Downloader:
    def __init__(self, url, depth_level) -> None:
        self.url = url
        self.depth_level = depth_level
        self.parsed_url = str(url)

    async def download_website(self):
        logger.info(f"Started downloading website contents of  {self.url}.")
        try:
            if not os.path.exists(downloaded_site_path):
                os.makedirs(downloaded_site_path)
            if not os.path.exists(os.path.join(downloaded_site_path, str(self.parsed_url))):
                download_log_file_path = "download.log"
                if os.path.exists(download_log_file_path):
                    os.remove(download_log_file_path)
                with open("v6/logs/download.log", "w") as log_file:
                    subprocess.run(
                        [
                            "wget",
                            "-v",
                            "--mirror",
                            "--convert-links",
                            "--adjust-extension",
                            "--page-requisites",
                            "--no-parent",
                            "-l",
                            self.depth_level,
                            self.parsed_url,
                            "-P",
                            downloaded_site_path,
                        ],
                        # capture_output=True,
                        stdout=log_file,
                        stderr=log_file,
                        text=True,
                    )
            print("############  download_finished   ########################")
        except Exception as e:
            python_exception.log_exception()
            raise Exception
