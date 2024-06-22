from app import app
from app.model import *
from flask import request
from utils.Result import *
from utils.AutoPage import auto_page
from flask_cors import CORS
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine

db = db
app = app
request = request


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/assets/<path:path>")
def send_js(path):
    return app.send_static_file("assets/" + path)


def create_controller():
    from . import api, auth, db_, log, script, super, project, Interceptor, admin
    CORS(app, cors_allowed_origins="*")
    return app
