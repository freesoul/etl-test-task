import logging
import elasticsearch
import elasticsearch.helpers
import base64

if __name__ == "__main__":
    from utils import configure_root_logger

    LOGGER = configure_root_logger()
else:
    LOGGER = logging.getLogger()


class ESClient:

    COMMUNES_INDEX_NAME = "communes"
    MAPPING_COMMUNES = {
        "properties": {
            "commune_cadastrale": {"type": "text"},
            "commune_administrative": {"type": "text"},
            "code_section": {"type": "text"},
            "nom_section": {"type": "text"},
            "nom_section_pretty": {"type": "text"},
            "code_abbreviation": {"type": "text"},
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

    def insert(self, data:list):
        data = [ 
            {
                "_id": base64.b64encode('_'.join(row.values()).encode()).decode('utf-8'),
                **row
            } for row in data
        ]
        elasticsearch.helpers.bulk(self.es, data, index=ESClient.COMMUNES_INDEX_NAME)

    def _ensure_index_exists(self):
        self.es.indices.delete(index=ESClient.COMMUNES_INDEX_NAME, ignore=[400, 404])
        indices = list(self.es.indices.get_alias("*").keys())
        if ESClient.COMMUNES_INDEX_NAME not in indices:
            logging.info("Creating index %s" % ESClient.COMMUNES_INDEX_NAME)
            self.es.indices.create(index=ESClient.COMMUNES_INDEX_NAME, mappings=ESClient.MAPPING_COMMUNES)
        else:
            logging.info("Found index %s" % ESClient.COMMUNES_INDEX_NAME)
