from flask import request, jsonify, Blueprint
from core.client import CommunesClient
from config import ES_HOST


class APIBase(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.communes_client = CommunesClient(ES_HOST)

    def get_client(self):
        return self.communes_client

    def api_fail(self, msg:str = None):
        ret = {"result": "fail"}
        if msg:
            ret["description"] = msg
        return jsonify(ret)

    def api_success(self, msg=None, data=None):
        ret = {"result": "success"}
        if msg:
            ret["description"] = msg
        if data:
            ret["data"] = data
        return jsonify(ret)
