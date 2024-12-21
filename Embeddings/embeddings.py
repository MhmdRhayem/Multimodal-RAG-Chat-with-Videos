import torch
from transformers import CLIPProcessor, CLIPModel

def clip_embedder(index_search="image"):
    class CLIPEmbedder(Embeddings):
        def __init__(self):
            super().__init__()
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
            self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self.max_length = 77  # Maximum token length for CLIP text input
    
        def truncate_text(self, text):
            inputs = self.processor.tokenizer(text, return_tensors="pt", truncation=False)
            input_ids = inputs["input_ids"][0]
            original_length = len(input_ids)

    return CLIPEmbedder()