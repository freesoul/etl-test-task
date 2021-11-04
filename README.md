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
* ElasticSearch. Two indexes/mappings:
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

# Improvements

* No swagger was included.
* The price of apparments was not included (only commune + rental prices)

# Running

Git clone.
Install composer and docker-compose if you do not have them.
You may need to `sudo chmod 666 /var/run/docker.sock`.
Run `docker-compose up` and you should have the API working on http://localhost:5000.

