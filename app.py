from utils import *
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
chain = None
embedder = None
table = None

@app.route("/select_embedding", methods=["POST"])
def select_embedding_model():
    try:
        global embedder
        data = request.json
        if "embedding_model" not in data:
            return jsonify({"error": "No embedding model specified"}), 400

        selected_embedding = data["embedding_model"]
        embedder = create_embedder(selected_embedding)
        return jsonify({"message": f"{selected_embedding} embeddings selected"})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
