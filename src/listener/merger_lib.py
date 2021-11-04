import pandas as pd


class Merger:
    def __init__(self, transformed_communes_csv: str, transformed_prices_rent_csv: str):
        self.transformed_communes_csv = transformed_communes_csv
        self.transformed_prices_rent_csv = transformed_prices_rent_csv
        self.data = None

    def get_processed(self):
        if not self.data is None:
            return self.data

        df_communes = pd.read_csv(self.transformed_communes_csv).fillna("")
        df_rent = pd.read_csv(self.transformed_prices_rent_csv).fillna("")

        for numeric_column in ["rent_m2", "num_offer", "rent_abs"]:
            df_rent[[numeric_column]] = df_rent[[numeric_column]].apply(pd.to_numeric, errors='coerce').fillna(0)

        data_communes_dict = {}  # to group sections
        for idx, row in df_communes.iterrows():
            if row["commune_cadastrale"] not in data_communes_dict.keys():
                data_communes_dict[row["commune_cadastrale"]] = {
                    "commune_administrative": row["commune_administrative"],
                    "code_abbreviation": row["code_abbreviation"],
                    "sections": [],
                }
            data_communes_dict[row["commune_cadastrale"]]["sections"].append(
                {
                    "code_section": row["code_section"],
                    "nom_section": row["nom_section"],
                    "nom_section_pretty": row["nom_section_pretty"],
                }
            )

        data_communes = [{"commune": commune, **infos} for commune, infos in data_communes_dict.items()]
        data_rent = df_rent.to_dict('records')
        return data_communes, data_rent


if __name__ == "__main__":
    merger = Merger("data/transformed/communes.csv", "data/transformed/prices_rent.csv")
    merger.get_processed()