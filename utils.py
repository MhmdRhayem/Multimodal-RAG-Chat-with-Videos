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
    

