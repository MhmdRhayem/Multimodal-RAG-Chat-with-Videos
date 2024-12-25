import gradio as gr
import requests
import shutil
import os

API_URL = "http://127.0.0.1:5000"
HISTORY = ""

def select_embedding(embedding_model):
    gr.Info("Selecting embedding model ...")
    data = {"embedding_model": embedding_model}
    response = requests.post(f"{API_URL}/select_embedding", json=data)
    
    print("Embedding model selected.")
    if response.status_code != 200:
            return f"Error: {response.text}"
        
    
    gr.Info("Embedding model selected.")
    return [f"Embedding model '{embedding_model}' selected.", gr.update(interactive=True)]

def save_video(video):
    video_folder = "./videos"
    os.makedirs(video_folder, exist_ok=True)

    # `video` is the path to the uploaded file
    if video is not None:
        video_name = "video.mp4"
        video_path = os.path.join(video_folder, video_name)
        
        # Save the video file in the designated folder
        shutil.move(video, video_path)  # Move the uploaded video to the folder
        return f"Video '{video_name}' saved successfully at {video_path}."
    else:
        return "Please upload a video."


def upload_video(video):
    save_video(video)
    print("Video uploaded successfully.")
    
    gr.Info("Wait while preprocessing the video ...")
    print("Preprocessing video...")
    response = requests.post(f"{API_URL}/video_preprocessing")
    
    gr.Info("Wait while creating the vector store ...")
    print("Creating vector store...")
    response = requests.post(f"{API_URL}/create_vector_store")
    
    gr.Info("Ready to ask a question.")
    return ["Video uploaded and preprocessed successfully.", gr.update(interactive=True)]
    
    
def generate_results(query):
    global HISTORY
    data = {"query": query}
    gr.Info("Generating results ...")
    response = requests.post(f"{API_URL}/answer_question", json=data)
    result = response.json()
    print(f"RESULT: {result}")
    description = result["description"]
    output_video_path = result["output_video_path"]
    
    HISTORY += f"Query: {query}\nResponse: {description}\n\n"
    gr.Info("Results generated.")
    return [HISTORY, output_video_path]