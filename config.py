import os

mysql_config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'supersql',
    'user': 'supersql',
    'password': 'bQDDCBx2EkbGfaHW'
}

mysql_uri = (f"mysql+pymysql:/"
             f"/{mysql_config.get('user')}"
             f":{mysql_config.get('password')}"
             f"@{mysql_config.get('host')}"
             f":{str(mysql_config.get('port'))}"
             f"/{mysql_config.get('database')}")

jwt_config = {
    "secretkey": "ehjfsdfvfksgfigwehfvkfhvksd"
}

class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mydatabase.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = mysql_uri
