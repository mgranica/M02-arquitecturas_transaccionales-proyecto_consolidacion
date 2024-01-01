from flask import Flask, g
from sqlalchemy import create_engine
import os
import json


def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = get_sqlalchemy_db_uri()
    app.db_engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])  
    app.credentials = get_credentials()
    # existing code omitted
    from . import views
    app.register_blueprint(views.bp)
    
    @app.teardown_appcontext
    def teardown_db(exception=None):
        # Close the database connection at the end of the request
        if hasattr(g, 'db_engine'):
            g.db_engine.dispose()

    return app

def get_sqlalchemy_db_uri():
    ## TODO docker environment definition
    host = os.environ.get("HOST_APP",'localhost')
    database = os.environ.get("DATABASE_APP",'Pictures')
    user = os.environ.get("USER_APP",'mbit')
    password = os.environ.get("PASSWORD_APP",'mbit')
    
    return f"mysql+pymysql://{user}:{password}@{host}/{database}"

def get_credentials():
    credentials_path = os.environ.get("CREDENTIAL_PATH", "./credentials.json")
    # Load credentials from the JSON file
    with open(credentials_path, 'r') as file:
        credentials = json.load(file)
    return credentials