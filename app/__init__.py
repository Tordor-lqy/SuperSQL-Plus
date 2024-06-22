from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy()
db.init_app(app)




def create_app():
    with app.app_context():
        from . import routes

    return app
