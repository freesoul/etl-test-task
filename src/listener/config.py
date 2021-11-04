
RAW_DIR = "data/raw"
TRANSFORMED_DIR = "data/transformed"

DATA_SOURCES = {
    "communes" : {
        "url": "https://data.public.lu/en/datasets/r/15304974-6ea1-4e19-b368-8f20278d0eca",
        "format" : "xlsx",
        "first_value" : (5, 0),
    },
    "prices_rent" : {
        "url": "https://data.public.lu/fr/datasets/r/94e4a229-c564-4dd2-99b5-6b6e9d29eafd",
        "format": "xls",
        "first_value": (0, 2),
        "sheets" : [str(sheet) for sheet in list(range(2009, 2021))],
        "skip_until": "Commune",
        "stop_on": "nan",
        "columns": ["year", "commune", "num_offer", "rent_abs", "rent_m2"],
    }
}

ES_HOST = 'localhost'