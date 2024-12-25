import requests
import shutil
import os

API_URL = "http://127.0.0.1:5000"
UPLOADED_VIDEO_PATH = "./videos/video.mp4"
HISTORY = ""

def select_embedding(embedding_model):
    data = {"embedding_model": embedding_model}
    response = requests.post(f"{API_URL}/select_embedding", json=data)
    
    print("Embedding model selected.")
    if response.status_code != 200:
            return f"Error: {response.text}"
    
    return f"Embedding model '{embedding_model}' selected."

def upload_video():
    pass

def generate_results():
    pass