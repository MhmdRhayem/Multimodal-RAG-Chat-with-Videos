import requests
import os
from pytubefix import YouTube, Stream
from tqdm import tqdm
import glob
import whisper
from moviepy import VideoFileClip
import re
import json
import cv2
import shutil
import ollama
import torch

def download_video_from_url(video_url=video_url, path="./videos", filename="video.mp4"):
    try:
        yt = YouTube(video_url)

        streams = yt.streams.filter(progressive=True, file_extension="mp4")

        highest_res_stream = streams.order_by("resolution").desc().first()

        if not os.path.exists(path):
            os.makedirs(path)

        highest_res_stream.download(output_path=path, filename=filename)
        print(f"Download is completed successfully. File saved as {path}/{filename}")

    except Exception as err:
        # Print the error message if an error occurs
        print(f"An error has occurred: {err}")


def extract_subtitles_from_video(video_path="./videos/video.mp4", subtitle_format="srt", save_segments=True):

    try:
        subtitle_path = "./subtitles"
        results_path = "./videos"
        
        if not os.path.exists(subtitle_path):
            os.makedirs(subtitle_path)
        
        audio_path = "./audio/audio.mp3"
        
        if not os.path.exists(os.path.dirname(audio_path)):
            os.makedirs(os.path.dirname(audio_path))
        
        video = VideoFileClip(video_path)
        
        video.audio.write_audiofile(audio_path, codec="libmp3lame")

        model = whisper.load_model("small")
        
        print("Transcribing audio using Whisper...")
        result = model.transcribe(audio_path)
        
        results_file = os.path.join(results_path, "results.json")
        
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"Full result saved at {result_file}")
        
        if subtitle_format not in ["srt", "vtt"]:
            raise ValueError("Invalid subtitle format. Choose 'srt' or 'vtt'.")

        extension = "srt" if subtitle_format == "srt" else "vtt"
        
        subtitle_file = os.path.join(subtitle_path, f"subtitles.{extension}")
        
        with open(subtitle_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                start_time = format_time(segment["start"], subtitle_format)
                end_time = format_time(segment["end"], subtitle_format)
                
                if subtitle_format == "srt":
                    f.write(f"{i + 1}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['text']}\n\n")
                    
                elif subtitle_format == "vtt":
                    if i == 0:
                        f.write("WEBVTT\n\n") 
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['text']}\n\n")
                    
                print(f"Subtitle generation completed successfully. Subtitles saved at {subtitle_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def format_time(seconds, subtitle_format):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    if subtitle_format == "srt":
        return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"
    elif subtitle_format == "vtt":
        return f"{hours:02}:{minutes:02}:{int(seconds):02}.{milliseconds:03}"

def is_speech(result_file="./videos/result.json", no_speech_prob=0.5, min_duration=1.0):
    try:
        with open(result_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        segments = result["segments"]
        
        speech_count = 0
        
        for segment in segments:
            duration = segment["end"] - segment["start"]
            if duration >= min_duration and segment["no_speech_prob"] <= no_speech_prob:
                speech_count += 1

        if speech_count > len(result["segments"]) / 2:
            print(f"Speech detected.")
            return True
        else:
            print("No valid speech detected in transcript.")
            return False
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def extract_and_save_frames_and_metadata_with_speech(video_path="./videos/video.mp4", results_path="./videos/result.json"):
    path_to_save_frames = "./videos/extracted_frames"
    path_to_save_metadata = "./videos/metadata"
    
    if os.path.exists(path_to_save_frames):
        shutil.rmtree(path_to_save_frames)
    os.makedirs(path_to_save_frames)
    
    if not os.path.exists(path_to_save_metadata):
        os.makedirs(path_to_save_metadata)
        
    # Load Video
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Error: Cannot open video file.")
        return
    
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    metadatas = []
    for result in results["segments"]:
        id = result["id"]
        start_time = s2ms(result["start"])
        end_time = s2ms(result["end"])
        mid_time = (start_time + end_time) / 2
        
        # Set video position to mid_time
        video.set(cv2.CAP_PROP_POS_MSEC, mid_time)

        # Read the frame at mid_time
        success, frame = video.read()

        if success:
            text = result["text"]
            frame_filename = f"{path_to_save_frames}/frame_{id}.jpg"
            cv2.imwrite(frame_filename, frame)
            
            metadata = {
                "extracted_frame_path": frame_filename,
                "transcript": text,
                "video_segment_id": id,
                "video_path": video_path,
                "start_time_ms": start_time,
                "mid_time_ms": mid_time,
                "end_time_ms": end_time,
            }
            metadatas.append(metadata)
            
        else:
            print(f"ERROR! Cannot extract frame: id = {id}")

    video.release()
    
    transcripts = [vid["transcript"] for vid in metadatas]
    augmented_transcripts = augment_transcripts(transcripts, n=7)
    
    for idx, metadata in enumerate(metadatas):
        metadata["text"] = augmented_transcripts[idx]
        
    metadata_file = os.path.join(path_to_save_metadata, "metadata.json")

    with open(metadata_file, "w", encoding="utf-8") as metadata_file:
        json.dump(metadatas, metadata_file, indent=4)
        
    print("Frames and metadata extraction complete.")
    return metadatas


def s2ms(seconds):
    seconds = float(seconds)
    total_milliseconds = seconds * 1000
    return total_milliseconds

def augment_transcripts(trans_arr, n=7):
    updated_trans_arr = [
        (
            " ".join(trans_arr[i - int(n / 2) : i + int(n / 2)])
            if i - int(n / 2) >= 0
            else " ".join(trans_arr[0 : i + int(n / 2)])
        )
        for i in range(len(trans_arr))
    ]
    return updated_trans_arr

def extract_and_save_frames_and_metadata_without_speech(video_path="./videos/no_speech.mp4",results_path="./videos/result.json",num_of_extracted_frames_per_second=0.5):
    path_to_save_frames = "./videos/extracted_frames"
    path_to_save_metadata = "./videos/metadata"
    
    if os.path.exists(path_to_save_frames):
        shutil.rmtree(path_to_save_frames)
    os.makedirs(path_to_save_frames)
    
    if not os.path.exists(path_to_save_metadata):
        os.makedirs(path_to_save_metadata)
        
    # Load Video
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print("Error: Cannot open video file.")
        return

    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    metadatas = []
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration_ms = int(total_frames / fps * 1000)  # Total duration in milliseconds
    hop = round(fps / num_of_extracted_frames_per_second)
    half_hop_ms = s2ms(hop / fps / 2)  
    
    curr_frame = 0
    id = -1
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if curr_frame % hop == 0:
            id += 1
            mid_time_ms = s2ms(curr_frame / fps)
            start_time_ms = max(0, mid_time_ms - half_hop_ms) 
            end_time_ms = min(video_duration_ms, mid_time_ms + half_hop_ms)
            
            img_fname = f"frame_{id}.jpg"
            img_fpath = os.path.join(path_to_save_frames, img_fname)
            cv2.imwrite(img_fpath, image)
            
def get_image_description_ollama(image_path):
    content = """You are an assistant tasked with summarizing images for optimal retrieval. \
    These summaries will be embedded and used to retrieve the raw image.
    Write a clear and concise summary that captures all the important information"""
    message = {"role": "user", "content": content, "images": [image_path]}
    
    try:
        response = ollama.chat(model="llava:7b", messages=[message])
        description = response["message"]["content"]
        return description
    except Exception as e:
        print(f"Error: {e}")
        return "No description available."