from gradio_utils import *

with gr.Blocks() as app:
    gr.Markdown("### RAG Chat with Videos")

    embedding_choice = gr.Dropdown(
        ["huggingface", "ollama", "openai"], label="Select Embedding Model"
    )
    
    with gr.Blocks() as app:
        gr.Markdown("### RAG Document Question-Answering System")

        embedding_choice = gr.Dropdown(
            ["bridgetower","clip-text","clip-image"], label="Select Embedding Model"
        )