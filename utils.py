from embeddings.embeddings import clip_embedder, bridgetower_embedder
import pandas as pd
import lancedb
from langchain_core.runnables import (
    RunnableParallel, 
    RunnablePassthrough, 
    RunnableLambda
)
import warnings
import json
from vectorstore.vectorstore import *
import ollama
from moviepy import VideoFileClip

warnings.filterwarnings("ignore")

def create_embedder(embedding_model="bridgetower"):
    try:
        embedding_model = embedding_model.lower()
        if embedding_model == "clip-text":
            return clip_embedder(index_search= "text")
        elif embedding_model == "clip-image":
            return clip_embedder(index_search= "image")
        elif embedding_model == "bridgetower":
            return bridgetower_embedder()
        else:
            raise ValueError("Invalid embedder type. Choose from 'clip' or 'bridgetower'.")
        print("Embedder created successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_metadata():
    try:
        with open("./videos/metadata/metadata.json") as f:
            metadata = json.load(f)
        print("Metadata loaded successfully.")
        return metadata
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def create_db_from_text_image_pairs(embedder):
    try:
        metadata = get_metadata()
        
        texts = [data["text"] for data in metadata]
        image_paths = [data["extracted_frame_path"] for data in metadata]
        
        db = lancedb.connect("./vectorstore/lancedb")
        _ = MultimodalLanceDB.from_text_image_pairs(
            texts=texts,
            image_paths=image_paths,
            embedding=embedder,
            metadatas=metadata,
            connection=db,
            table_name="MULTIRAGTABLE",
            mode="overwrite",
        )
        print("Database created successfully.")
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def get_table_from_db():
    try:
        db = lancedb.connect("./vectorstore/lancedb")
        table = db.open_table("MULTIRAGTABLE")
        print("Table loaded successfully.")
        return table
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def retreive_results(input):
    table = input["table"]
    embedder = input["embedder"]
    query = input["query"]
    try:
        if table is None:
            get_table_from_db()
        query_embeddings = embedder.embed_query(query)
        results = table.search(query_embeddings).limit(1).to_list()
        print("Done Retreiving Results")
        return results
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Chain Components
def prompt_processing(input):
    # Get the retrieved results and user's query
    retrieved_results = input['retrieved_results']
    user_query = input['user_query']['query']
    
    retrieved_result = retrieved_results[0]
    prompt_template = (
        "The transcript associated with the image is '{transcript}'. "
        "{user_query}"
        "Don't mention anything about the image quality in your response."
        "Try to answer that in a maximum of 3 sentences."
    )
    
    retrieved_metadata = retrieved_result['metadata']
    transcript = retrieved_metadata['text']
    frame_path = retrieved_metadata['extracted_frame_path']
    prompt = prompt_template.format(
            transcript=transcript, 
            user_query=user_query
        )
    message = {
        "role": "user",
        "content": prompt,
        "images": [frame_path]
    }
    midtime = retrieved_metadata["mid_time_ms"]
    answer = {
        "message": message,
        "midtime": midtime
    }
    print("Done Processing Prompt")
    return answer

def LVLM(input):
    message = input["message"]
    midtime = input["midtime"]
    response = ollama.chat(model="llava:7b", messages=[message])
    description = response["message"]["content"]
    image = message["images"][0]
    print("Done Generating Description")
    output = {"image": image, "description":description, "midtime" : midtime}
    return output

def generate_video(input):
    midtime = input["midtime"]
    video_path = "./videos/video.mp4"  # Assuming video path is fixed or can be parameterized
    output_video_path = "./videos/video_temp.mp4"
    play_before_sec = 3
    play_after_sec = 3
    input["video_path"] = video_path
    input["output_video_path"] = output_video_path
    try:
        timestamp_in_sec = int(float(midtime) / 1000)
        print(timestamp_in_sec)
        with VideoFileClip(video_path) as video:
            duration = video.duration
            start_time = max(timestamp_in_sec - play_before_sec, 0)
            end_time = min(timestamp_in_sec + play_after_sec, duration)
            new = video.subclipped(start_time, end_time)
            new.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
        print("Done Generating Video Clip")
        return input
    except Exception as e:
        print(f"An error occurred during video generation: {e}")
        return input

def create_multirag_chain():
    mm_rag_chain = (
    RunnableParallel({
        "retrieved_results": RunnableLambda(retreive_results), 
        "user_query": RunnablePassthrough()
    }) 
    | RunnableLambda(prompt_processing)
    | RunnableLambda(LVLM)
    | RunnableLambda(generate_video)
)
    return mm_rag_chain