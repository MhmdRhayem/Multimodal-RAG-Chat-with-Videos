import torch
from transformers import CLIPProcessor, CLIPModel

def clip_embedder(index_search="image"):
    class CLIPEmbedder(Embeddings):
        pass
    return CLIPEmbedder()