RAW_DIR = "data/raw"
TRANSFORMED_DIR = "data/transformed"

DATA_SOURCES = {
    "communes": {
        "url": "https://data.public.lu/en/datasets/r/15304974-6ea1-4e19-b368-8f20278d0eca",
        "format": "xlsx",
        "first_value": (6, 0), # row, col
        "columns": [
            "commune_cadastrale",
            "commune_administrative",
            "code_section",
            "nom_section",
            "nom_section_pretty",
            "code_abbreviation",
        ],
    },
    "prices_rent": {
        "url": "https://data.public.lu/fr/datasets/r/94e4a229-c564-4dd2-99b5-6b6e9d29eafd",
        "format": "xls",
        "first_value": (0, 2), # row, col
        "sheets": [str(sheet) for sheet in list(range(2009, 2021))],
        "skip_until": "Commune",
        "stop_on": "nan",
        "columns": ["year", "commune", "num_offer", "rent_abs", "rent_m2"],
    },
}

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASS = "guest"
RABBITMQ_QUEUE = "communes_polling_queue"

ES_HOST = "localhost"
ES_MAPPINGS = {
    "communes": {
        "properties": {
            "commune_cadastrale": {"type": "text"},
            "commune_administrative": {"type": "text"},
            "code_abbreviation": {"type": "text"},
            "sections": {
                "type": "nested",
                "properties": {
                    "code_section": {"type": "text"},
                    "nom_section": {"type": "text"},
                    "nom_section_pretty": {"type": "text"},
                },
            },
        }
    },
    "communes_rentals": {
        "properties": {
            "commune_administrative": {"type": "text"},
            "year": {"type": "integer"},
            "num_offer": {"type": "integer"},
            "rent_abs": {"type": "float"},
            "rent_m2": {"type": "float"},
        },
    },
}