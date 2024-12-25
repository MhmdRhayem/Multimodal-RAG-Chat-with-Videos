import gradio as gr 
from gradio_utils import *

with gr.Blocks() as app:
    gr.Markdown("### RAG Chat with Videos")

    embedding_choice = gr.Dropdown(
        ["bridgetower", "clip-text", "clip-image"], label="Embedding Model", value= None
    )
    output_text = gr.Textbox(label="Output", visible=True)
    
    embedding_choice.change(
        fn=select_embedding,
        inputs=[embedding_choice],
        outputs=[output_text],
        show_progress=True, 
    )
app.launch()