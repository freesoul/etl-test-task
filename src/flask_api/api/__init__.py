import os

import pika

from flask import Blueprint, jsonify, request
from core.client import CommunesClient
from api.common.apibase import APIBase
from config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_QUEUE

app = APIBase("Communes", __name__)


@app.route("/", methods=["GET"])
def get_commune():
    include_rents = request.args.get("include_rents", default=True, type=bool)
    client = app.get_client()
    response = client.getCommunes(include_rents=include_rents)
    return app.api_success(None, response)


@app.route("/<commune>", methods=["GET"])
def get_commune_by_name(commune:str):
    include_rents = request.args.get("include_rents", default=True, type=bool)
    client = app.get_client()
    response = client.getCommunes(commune=commune, include_rents=include_rents)
    return app.api_success(None, response)


@app.route(
    "/download-and-insert",
    methods=["GET", "POST"],
)
def download_and_insert():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body="")
    connection.close()
    return app.api_success(None, [])


# @app.route(
#     "/get-status",
#     methods=["GET"],
# )
# def get_status():
#     client = app.get_client()
#     return app.api_success(None, [])
