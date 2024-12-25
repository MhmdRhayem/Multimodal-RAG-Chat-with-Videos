from gradio_utils import *

with gr.Blocks() as app:
    gr.Markdown("### RAG Chat with Videos")

    embedding_choice = gr.Dropdown(
        ["huggingface", "ollama", "openai"], label="Select Embedding Model"
    )
    
