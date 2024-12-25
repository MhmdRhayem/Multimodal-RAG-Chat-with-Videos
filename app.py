from utils import *
from videos.video_preprocessing import *
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

@app.route("/video_preprocessing", methods=["POST"])
def video_preprocessing():
    try:
        # extract_subtitles_from_video()
        print("Done extracting subtitles from video")
        
        is_speech = contain_speech()
        if is_speech:
            # extract_and_save_frames_and_metadata_with_speech()
            print("Done extracting frames and metadata with speech")
        else:
            extract_and_save_frames_and_metadata_without_speech()
            embedder = create_embedder("clip-image")
            print("Done extracting frames and metadata without speech")
        
        return jsonify({"message": "Video preprocessing completed"}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@app.route("/create_vector_store",methods = ["POST"])
def create_store():
    try:
        global table, embedder
        if embedder is None:
            return jsonify({"error": "No embedding model selected"}), 400
        print("Creating vector store ...")
        create_db_from_text_image_pairs(embedder)
        print("Getting table ...")
        table = get_table_from_db()
        return jsonify({"message": "Vector store created"}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@app.route("/generate_results", methods=["POST"])
def generate_results():
    try:
        pass
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
