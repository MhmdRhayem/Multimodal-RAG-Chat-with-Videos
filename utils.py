from embeddings.embeddings import clip_embedder, bridgetower_embedder

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
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")