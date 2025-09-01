from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.cahtntfghqaepqubnaua:lavjain91405@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:wafzafar@localhost:5432/crud"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False 

app.secret_key = "supersecret123"

db = SQLAlchemy(app)

