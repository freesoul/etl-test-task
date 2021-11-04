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
    def __init__(self, host: str, mappings: dict):
        self.es = elasticsearch.Elasticsearch(
            [
                {"host": host},
            ],
            timeout=300,
        )
        self.mappings = mappings
        self._ensure_indexes_exist()

    def insertCommunes(self, data: list):
        # id is base64 of everything related to the commune (therefore excepting sections)
        data = [{"_id": base64.b64encode("_".join(list(row.values())[:3]).encode()).decode("utf-8"), **row} for row in data]
        elasticsearch.helpers.bulk(self.es, data, index="communes")

    def insertRentals(self, data: list):
        # _id is base64 of year + commune
        data = [{"_id": base64.b64encode(("%s_%s" % (row["commune"], str(row["year"]))).encode()).decode("utf-8"), **row} for row in data]
        elasticsearch.helpers.bulk(self.es, data, index="communes_rentals")

    def _ensure_indexes_exist(self):
        existing_indices = list(self.es.indices.get_alias("*").keys())
        for index, mapping in self.mappings.items():
            # self.es.indices.delete(index=index, ignore=[400, 404])
            if index not in existing_indices:
                logging.info("Creating index %s" % index)
                self.es.indices.create(index=index, mappings=mapping)
            else:
                logging.info("Found index %s" % index)
