import gradio as gr
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

def save_video(video):
    video_folder = "./videos"
    os.makedirs(video_folder, exist_ok=True)

    # `video` is the path to the uploaded file
    if video is not None:
        video_name = "video.mp4"
        video_path = os.path.join(video_folder, video_name)
        
        # Save the video file in the designated folder
        shutil.move(video, video_path)  # Move the uploaded video to the folder
        output = f"Video '{video_name}' saved successfully at {video_path}."
        print(output)
        return output
    else:
        return "Please upload a video."


def upload_video(video):
    save_video(video)
    Print("Video uploaded successfully.")
    
    gr.Info("Wait while preprocessing the video ...")
    Print("Preprocessing video...")
    response = requests.post(f"{API_URL}/video_preprocessing")
    
    gr.Info("Wait while creating the vector store ...")
    Print("Creating vector store...")
    response = requests.post(f"{API_URL}/create_vector_store")
    
    return "Video uploaded and preprocessed successfully."
    
    
def generate_results():
    pass