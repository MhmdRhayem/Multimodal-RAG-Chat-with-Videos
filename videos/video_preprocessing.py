import requests
import os
from pytubefix import YouTube, Stream


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
        
        
    except Exception as e:
        print(f"An error occurred: {e}")

