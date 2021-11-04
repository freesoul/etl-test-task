# What is included
It includes 2 services:
* RabbitMQ
* ElasticSearch

And 2 custom services:
* A rabbitmq listener which downloads, transforms and inserts into ES the test task data.
* An API which has a route to trigger the previous, and to retrieve the data.

# Running it

## Preliminary steps
Give permissions `sudo chmod 666 /var/run/docker.sock`

## Finally
Run `docker-compose up` and you should have the API working on http://localhost:5000.