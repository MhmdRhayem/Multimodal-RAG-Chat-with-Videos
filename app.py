from utils import *
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
chain = None
embedder = None
table = None

@app.route("/select_embedding", methods=["POST"])
def select_embedding_model():
    pass

