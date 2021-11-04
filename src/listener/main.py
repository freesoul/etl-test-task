import os
import logging
from es_client import ESClient
import pika
from config import ES_HOST, ES_MAPPINGS, RAW_DIR, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_QUEUE
from downloader_lib import Downloader
from merger_lib import Merger


if __name__ == "__main__":
    from utils import configure_root_logger

    LOGGER = configure_root_logger()
else:
    LOGGER = logging.getLogger()


def callback(ch, method, properties, body):
    # we don't really care about the body.
    LOGGER.info("Received a request")

    downloader = Downloader()
    downloader.download()  # This calls the format transformer inside.

    assert os.path.isfile("data/transformed/communes.csv"), "communes.csv not found"
    assert os.path.isfile("data/transformed/prices_rent.csv"), "prices_rent.csv not found"

    merger = Merger("data/transformed/communes.csv", "data/transformed/prices_rent.csv")
    communes, rental_prices = merger.get_processed()

    client = ESClient(ES_HOST, ES_MAPPINGS)
    client.insertCommunes(communes)
    client.insertRentals(rental_prices)
    LOGGER.info("Done")


if __name__ == "__main__":

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, "/", pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS))
    )
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()