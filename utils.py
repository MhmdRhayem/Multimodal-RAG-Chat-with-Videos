from embeddings.embeddings import clip_embedder, bridgetower_embedder
import pandas as pd
import lancedb
from langchain_core.runnables import (
    RunnableParallel, 
    RunnablePassthrough, 
    RunnableLambda
)

def create_embedder(embedder_type="bridgetower"):
    try:
        embedder_type = embedder_type.lower()
        if embedder_type == "clip":
            return clip_embedder()
        elif embedder_type == "bridgetower":
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
        
def create_db_from_text_image_pairs(embedder_type="bridgetower"):
    try:
        embedder = create_embedder(embedder_type)
        metadata = get_metadata()
        
        texts = [data["text"] for data in metadata]
        image_paths = [data["extracted_frame_path"] for data in metadata]
        
        db = lancedb.connect("./lancedb")
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
        db = lancedb.connect("./lancedb")
        table = db.open_table("MULTIRAGTABLE")
        print("Table loaded successfully.")
        return table
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def retreive_results(table, embedder, query):
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
    user_query = input['user_query']
    
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
    return image, description, midtime

def create_multirag_chain():
    mm_rag_chain = (
    RunnableParallel({
        "retrieved_results": RunnableLambda(retreive_results), 
        "user_query": RunnablePassthrough()
    }) 
    | RunnableLambda(prompt_processing)
    | RunnableLambda(LVLM)
)
    return mm_rag_chain

def generate_video_clip(timestamp_in_ms,video_path = "./videos/video.mp4", output_video = "./videos/video_temp.mp4", play_before_sec: int=3, play_after_sec: int=3):
    pass