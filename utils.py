from embeddings.embeddings import clip_embedder, bridgetower_embedder

def create_embedder(embedder_type="bridgetower"):
    try:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
