import os
import shutil
import subprocess
from urllib.parse import urlparse

from exceptions import SomethingWentWrong
from logger import configure_logging, logger
from utils.logger import PythonLoggerExtension

python_exception = PythonLoggerExtension()
configure_logging()


class Downloader:
    def __init__(self, url, depth_level) -> None:
        self.url = url
        self.depth_level = depth_level
        parsed_url = urlparse(url)
        self.domain = parsed_url.netloc
        self.url = str(url)
        self.downloaded_site_path = "downloaded_site"

    async def download_website(self):
        logger.info(f"Started downloading website contents of  {self.url}.")
        try:
            if not os.path.exists(self.downloaded_site_path):
                os.makedirs(self.downloaded_site_path)

            directory_path = os.path.join(self.downloaded_site_path, str(self.domain))
            if os.path.exists(directory_path) and os.path.isdir(directory_path):
                shutil.rmtree(directory_path)
            if not os.path.exists(directory_path):
                download_log_file_path = "download.log"
                if os.path.exists(download_log_file_path):
                    os.remove(download_log_file_path)
                with open("download.log", "w") as log_file:
                    subprocess.run(
                        [
                            "wget",
                            # "-v",   #verbose mode
                            "--mirror",
                            "--convert-links",
                            "--adjust-extension",
                            "--page-requisites",
                            "--no-parent",
                            "-l",
                            self.depth_level,
                            "--reject=mp4,avi,mov",  # Reject specific file types
                            self.url,
                            "-P",
                            self.downloaded_site_path,
                        ],
                        # capture_output=True,
                        stdout=log_file,
                        stderr=log_file,
                        text=True,
                    )
                print("-------------  download_finished  --------------")
        except Exception as e:
            python_exception.log_exception()
            raise SomethingWentWrong("Download failed")
