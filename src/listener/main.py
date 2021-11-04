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
    import csv

    data = []
    with open("data/transformed/limites.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        next(spamreader)  # skip reader
        for _row in spamreader:
            row = {
                "commune_cadastrale": _row[0],
                "commune_administrative": _row[1],
                "code_section": _row[2],
                "nom_section": _row[3],
                "nom_section_pretty": _row[4],
                "code_abbreviation": _row[5],
            }
            data.append(row)
    client.insert(data)
