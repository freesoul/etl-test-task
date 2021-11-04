
import logging
from es_client import ESClient

from config import ES_HOST

if __name__ == "__main__":
    from utils import configure_root_logger

    LOGGER = configure_root_logger()
else:
    LOGGER = logging.getLogger()


if __name__ == "__main__":
    client = ESClient(ES_HOST)
