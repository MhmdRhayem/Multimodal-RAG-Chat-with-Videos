# MultiRAG Chat with Videos

This repository implements a Multi-Retrieval-Augmented Generation (MultiRAG) system designed for interactive video-based question-answering. The system enables users to upload videos, ask questions about their content, and receive both textual answers and relevant video clips corresponding to their queries. It leverages cutting-edge vision-language models and embeddings for efficient processing and interaction through a Flask API and Gradio interface.

---

## Features

- **Video Upload and Processing**: Upload video files (`.mp4`, `.avi`, `.mov`, etc.) for content analysis and question answering.
- **Multiple Embedding Models**: Supports `BridgETower` and `CLIP` for video embeddings.
- **Vision Model Integration**: Uses `llava` (via Ollama) as the vision-language model to generate transcripts from videos.
- **Query Response**: Generates concise text answers along with short video clips corresponding to the query.
- **Interactive Gradio Interface**:Easily interact with the system through a user-friendly web app.

---

## Installation

### Prerequisites
- Python 3.8 or above
- [Ollama](https://ollama.com) installed for using the `llava` vision-language model.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/MhmdRhayem/MultiRAG-Chat-with-Videos
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the `llava` model using Ollama:
   ```bash
   ollama pull llava
   ```

4. Run the Flask backend:
   ```bash
   python app.py
   ```

5. Launch the Gradio app:
   ```bash
   python gradio_app.py
   ```

---

## Technologies Used
- **Backend:** Flask
- **Frontend:** Gradio
- **Embedding Models:** `BridgETower`, `CLIP`
- **Vector Store**: Lancedb
- **Vision-Language Model:** `llava`

---

## Preview
Below is a preview of the Gradio interface for the MultiRAG Chat with Videos system:

![Gradio Interface](./image.gif)
