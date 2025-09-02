from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SUPABASE_URI")
print(app.config["SQLALCHEMY_DATABASE_URI"])
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:wafzafar@localhost:5432/crud"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False 

app.secret_key = os.environ.get("SECRET")

db = SQLAlchemy(app)

