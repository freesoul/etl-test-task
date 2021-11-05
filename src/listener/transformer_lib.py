import os
import pathlib
import csv
import logging

import openpyxl
import pandas as pd

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
        info = DATA_SOURCES[name]
        file_in_path = self.raw_data_path / ("%s.%s" % (name, info['format']))
        file_out_path = self.transformed_data_path / ("%s.csv" % name)
        if force or not os.path.isfile(file_out_path):
            LOGGER.info("Transforming dataset: %s" % file_out_path)

            if info['format'] == "xlsx":

                with open(file_in_path, "rb") as fr:
                    wb = openpyxl.load_workbook(fr)
                    sh = wb.active
                    with open(file_out_path, "w") as f:
                        c = csv.writer(f)
                        if 'columns' in info.keys():
                            c.writerow(info['columns'])
                        for i_row, r in enumerate(sh.rows):
                            if i_row < info["first_value"][0]:
                                continue
                            c.writerow([cell.value for i_col, cell in enumerate(r) if i_col > info["first_value"][1]])

            elif info['format'] == "xls":
                parsed = []
                for sheet in info['sheets']:
                    df = pd.read_excel(io=file_in_path, sheet_name=sheet)
                    values = df.values.tolist()
                    reached_first_line = False
                    for row in values:
                        row_parsed = row[info['first_value'][1]:]
                        if reached_first_line:
                            if str(row_parsed[0]) == info['stop_on']:
                                break
                            row_parsed = [sheet, *row_parsed]
                            parsed.append(row_parsed)
                        elif not reached_first_line and info['skip_until'] in str(row_parsed[0]):
                            reached_first_line = True
                pd.DataFrame(parsed).to_csv(file_out_path, index=False, header=info['columns'])
        else:
            LOGGER.info("Using cached transformed dataset: %s" % file_out_path)


if __name__ == "__main__":
    transformer = Transformer()
    transformer.transform("communes", force=True)
