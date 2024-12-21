import torch
from transformers import CLIPProcessor, CLIPModel
from transformers import BridgeTowerProcessor, BridgeTowerForContrastiveLearning
from PIL import Image
from langchain_core.embeddings import Embeddings
from tqdm import tqdm

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
            if original_length > self.max_length:
                truncated_ids = input_ids[:self.max_length]
                truncated_text = self.processor.tokenizer.decode(truncated_ids, skip_special_tokens=True)
                print(f"Text truncated from {original_length} tokens to {self.max_length} tokens.")
                return truncated_text
            return text

        def embed_documents(self, texts):
            embeddings = []
            for text in texts:
                text = self.truncate_text(text)
                inputs = self.processor(text=text, return_tensors="pt", padding=True, truncation=True, max_length=self.max_length).to(self.device)
                with torch.no_grad():
                    outputs = self.model.get_text_features(**inputs)
                embedding = outputs.tolist()
                embeddings.append(embedding[0])
            return embeddings
        
        def embed_query(self, text: str) -> List[float]:
            return self.embed_documents([text])[0]
        
        def embed_image_text_pairs(self, texts, images, batch_size=2):
            assert len(texts) == len(images), "The length of captions should be equal to the length of images"

            embeddings = []
            for text, image_path in tqdm(zip(texts, images), total=len(texts)):
                text = self.truncate_text(text)
                image = Image.open(image_path).convert("RGB")
                inputs = self.processor(text=[text], images=[image], return_tensors="pt", padding=True, truncation=True, max_length=self.max_length)
                inputs = {key: val.to(self.device) for key, val in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.model(**inputs)

                text_embeddings = outputs.text_embeds[0].tolist()
                image_embeddings = outputs.image_embeds[0].tolist()
                if index_search == "image":
                    embedding = image_embeddings
                else:
                    embedding = text_embeddings
                embeddings.append(embedding)
            return embeddings

    return CLIPEmbedder()

def bridgetower_embedder():
    class BridgeTowerEmbedder(Embeddings):
        def __init__(self):
            super().__init__()
            self.model = BridgeTowerForContrastiveLearning.from_pretrained("BridgeTower/bridgetower-large-itm-mlm-itc")
            self.processor = BridgeTowerProcessor.from_pretrained("BridgeTower/bridgetower-large-itm-mlm-itc")   

    return BridgeTowerEmbedder()