
def download_video_from_url(video_url=video_url, path="./videos", filename="video.mp4"):
    try:
        yt = YouTube(video_url)
        
        streams = yt.streams.filter(progressive=True, file_extension="mp4")

        highest_res_stream = streams.order_by("resolution").desc().first()

    except Exception as err:
        # Print the error message if an error occurs
        print(f"An error has occurred: {err}")