import flask

app = flask.Flask(__name__)

from api import app as communes_api

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(communes_api, url_prefix="/v1/communes")

if __name__ == "__main__":
    app.run(host="0.0.0.0")