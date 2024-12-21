
def download_video_from_url(video_url=video_url, path="./videos", filename="video.mp4"):
    try:
        yt = YouTube(video_url)

    except Exception as err:
        # Print the error message if an error occurs
        print(f"An error has occurred: {err}")