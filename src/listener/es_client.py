import logging
import elasticsearch

if __name__ == "__main__":
    from utils import configure_root_logger

    LOGGER = configure_root_logger()
else:
    LOGGER = logging.getLogger()


class ESClient:

    COMMUNES_INDEX_NAME = "communes"
    MAPPING_COMMUNES = {
        "properties": {
            "show_id": {"type": "text"},
            "release_year": {"type": "integer"},
        }
    }

    def __init__(self, host: str):
        self.es = elasticsearch.Elasticsearch(
            [
                {"host": host},
            ],
            timeout=300,
        )
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        # self.es.indices.delete(index=ESClient.COMMUNES_INDEX_NAME, ignore=[400, 404])
        indices = list(self.es.indices.get_alias("*").keys())
        if ESClient.COMMUNES_INDEX_NAME not in indices:
            logging.info("Creating index %s" % ESClient.COMMUNES_INDEX_NAME)
            self.es.indices.create(index=ESClient.COMMUNES_INDEX_NAME, mappings=ESClient.MAPPING_COMMUNES)
        else:
            logging.info("Found index %s" % ESClient.COMMUNES_INDEX_NAME)
