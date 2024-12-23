from embeddings.embeddings import clip_embedder, bridgetower_embedder
import pandas as pd
import lancedb

def create_embedder(embedder_type="bridgetower"):
    try:
        embedder_type = embedder_type.lower()
        if embedder_type == "clip":
            return clip_embedder()
        elif embedder_type == "bridgetower":
            return bridgetower_embedder()
        else:
            raise ValueError("Invalid embedder type. Choose from 'clip' or 'bridgetower'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_metadata():
    try:
        with open("./videos/metadata/metadata.json") as f:
            metadata = json.load(f)
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
        return True
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False