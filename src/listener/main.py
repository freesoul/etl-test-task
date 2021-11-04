import os
import logging
from es_client import ESClient

from config import ES_HOST, ES_MAPPINGS, RAW_DIR
from downloader_lib import Downloader
from merger_lib import Merger


if __name__ == "__main__":
    from utils import configure_root_logger

    LOGGER = configure_root_logger()
else:
    LOGGER = logging.getLogger()


if __name__ == "__main__":

    downloader = Downloader()
    downloader.download()  # This calls the format transformer inside.

    assert os.path.isfile("data/transformed/communes.csv"), "communes.csv not found"
    assert os.path.isfile("data/transformed/prices_rent.csv"), "prices_rent.csv not found"

    merger = Merger("data/transformed/communes.csv", "data/transformed/prices_rent.csv")
    communes, rental_prices = merger.get_processed()

    client = ESClient(ES_HOST, ES_MAPPINGS)
    client.insertCommunes(communes)
    client.insertRentals(rental_prices)
