import os
import pathlib
import logging

import requests

from config import DATA_SOURCES, RAW_DIR
from transformer_lib import Transformer

if __name__ == "__main__":
    from utils import configure_root_logger

    LOGGER = configure_root_logger()
else:
    LOGGER = logging.getLogger()


class Downloader:
    def __init__(self):
        self.raw_data_path = pathlib.Path(__file__).parent / RAW_DIR
        self.transformer = Transformer()
        os.makedirs(self.raw_data_path, exist_ok=True)

    def download(self, transform: bool = True):
        for name, info in DATA_SOURCES.items():
            file_out_path = self.raw_data_path / ("%s.%s" % (name, info['format']))
            if not os.path.isfile(file_out_path):
                LOGGER.info("Requesting dataset: %s" % file_out_path)
                content = requests.get(info["url"], allow_redirects=True).content
                with open(file_out_path, "wb") as f:
                    f.write(content)
            else:
                LOGGER.info("Using cached dataset: %s" % file_out_path)
            if transform:
                self.transformer.transform(name)


if __name__ == "__main__":
    downloader = Downloader()
    downloader.download()