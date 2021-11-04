# Test task

Expected, by importance: 
* Combine communes X prices (all story from 2009 to 2020)
* ETL process to read the csv and store in elasticsearch.
* Elasticsearch data schema.
* A REST API capable of:
    * Start the index process
    *  Retrieve a city and its information.

Data sources:

* Limites administratives du Grand-Duché de Luxembourg
https://data.public.lu/en/datasets/limites-administratives-du-grand-duche-de-luxembourg/

* Loyers annoncés des logements - Par commune
https://data.public.lu/fr/datasets/loyers-annonces-des-logements-par-commune/#_

* Prix de vente des appartements - Par commune
https://data.public.lu/fr/datasets/prix-de-vente-des-appartements-par-commune/#_


# Task resolution

The solution consists in a docker, which includes:
* RabbitMQ
* ElasticSearch. Two indexes/mappings: (find in src/listener/config.py)
    * communnes. The sections are inserted as nested "sections", because we assume that they will always be recovered.
    * communes_rentals. These are in a separate index, and requested only when needed.
* Custom Flask API, which reads ElasticSearch, or triggers a RabbitMQ message.
    * http://localhost:9200/communes/download-and-insert
    * http://localhost:9200/communes/
    * http://localhost:9200/communes/Bertrange
    The last two routes handle adittionally a "include_rents" boolean query parameter (default true)
* Custom RabbitMQ consumer, which, on receiving a message, it triggers the next pipeline:
    * Downloading the .xls / .xlsx from government.
    * Reformatting them into easy to handle .csv
    * Transforming them to insert into the ElasticSearch mapping


Basically:
```
Flask api <---- ES <------.
    \                      \              ,---- HTTP to lux sites
     `----> RabbitMQ ---> Consumer <--Downloader <--- Transformer
                                ^--- Merger
                                ^--- Inserter
```

# Improvements

* No swagger was included.
* The price of apparments was not included (only commune + rental prices)
* File structure (eg. making a libs folderfor the listener)

# Consumer file structure
Under `src/listener` you will find:

* `config.py` Find here the ES mappings and so on.
* `main.py` This runs the listener
* `es_client.py` This creates the mapping and inserts the data into the indices
* `downloader_lib.py` This downloads the files in config.py and reformats them (xls/xlsx -> csv). Before formatting they are in data/raw. After, in data/transformed.
* `merger_lib.py` This reads the files in data/transformed, and manipulates the structure to be suitable for the mappings.
* `transformer_lib.py` The helper which is used by downloader

# Running

Git clone.
Install composer and docker-compose if you do not have them.
You may need to `sudo chmod 666 /var/run/docker.sock`.
Run `docker-compose up` and you should have the API working on http://localhost:5000.

