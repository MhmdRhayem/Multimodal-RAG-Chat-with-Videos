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

@app.route("/create_vector_store",methods = ["POST"])
def create_store():
    try:
        global table, embedder
        if embedder is None:
            return jsonify({"error": "No embedding model selected"}), 400
        create_db_from_text_image_pairs(embedder)
        table = get_table_from_db()
        return table
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    
@app.route("/upload", methods=["POST"])
def upload_video():
    pass

@app.route("/generate_results", methods=["POST"])
def generate_results():
    try:
        pass
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500