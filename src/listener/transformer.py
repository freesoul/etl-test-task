import os
import pathlib
import csv
import logging

import requests
import openpyxl

from config import DATA_SOURCES, RAW_DIR, TRANSFORMED_DIR

if __name__ == "__main__":
    from utils import configure_root_logger

    LOGGER = configure_root_logger()
else:
    LOGGER = logging.getLogger()


class Transformer:
    def __init__(self):
        self.raw_data_path = pathlib.Path(__file__).parent / RAW_DIR
        self.transformed_data_path = pathlib.Path(__file__).parent / TRANSFORMED_DIR
        os.makedirs(self.raw_data_path, exist_ok=True)
        os.makedirs(self.transformed_data_path, exist_ok=True)

    def transform(self, name: str, force: bool = False):
        for name, info in DATA_SOURCES.items():
            file_in_path = self.raw_data_path / ("%s.xlsx" % name)
            file_out_path = self.transformed_data_path / ("%s.csv" % name)
            if force or not os.path.isfile(file_out_path):
                LOGGER.info("Transforming dataset: %s" % file_out_path)
                wb = openpyxl.load_workbook(file_in_path)
                sh = wb.active
                with open(file_out_path, "w") as f:
                    c = csv.writer(f)
                    reached_first_line = False
                    for i_row, r in enumerate(sh.rows):
                        if i_row < info["first_value"][0]:
                            continue
                        c.writerow([cell.value for i_col, cell in enumerate(r) if i_col > info["first_value"][1]])
            else:
                LOGGER.info("Using cached transformed dataset: %s" % file_out_path)


if __name__ == "__main__":
    transformer = Transformer()
    transformer.transform("limites", force=True)
