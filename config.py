from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SUPABASE_DATABASE_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:wafzafar@localhost:5432/crud"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False 

app.secret_key = "supersecret123"

db = SQLAlchemy(app)

