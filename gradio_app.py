import gradio as gr 
from gradio_utils import *

with gr.Blocks() as app:
    gr.Markdown("### RAG Chat with Videos")

    embedding_choice = gr.Dropdown(
        ["bridgetower", "clip-text", "clip-image"], label="Embedding Model", value= None
    )
    
    with gr.Row():
        video_input = gr.Video(label="Upload a Video")
        upload_button = gr.Button("Upload", interactive=False) 
    
    question_input = gr.Textbox(label="Ask a Question")
    submit_button = gr.Button("Submit", interactive=True)
    
    video_output = gr.Video(label="Output Video")

    output_text = gr.Textbox(label="Output", visible=True)
    
    embedding_choice.change(
        fn=select_embedding,
        inputs=[embedding_choice],
        outputs=[output_text, upload_button],
        show_progress=True, 
    )
    
    upload_button.click(
        fn = upload_video,
        inputs=[video_input],
        outputs = [output_text, submit_button],
    )
    
    submit_button.click(
        fn=generate_results,
        inputs=[question_input],
        outputs=[output_text, video_output],
    )
    
app.launch()