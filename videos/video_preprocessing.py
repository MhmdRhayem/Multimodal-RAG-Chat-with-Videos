import requests
import os
from pytubefix import YouTube, Stream
from tqdm import tqdm
import glob
import whisper
from moviepy import VideoFileClip
import re
import json

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
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False