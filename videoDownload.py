from pytube import YouTube
import os


def download_video(video_id, video_name):
    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
    stream = yt.streams.filter(res="480p").first()
    out_file = stream.download()
    os.rename(out_file, video_name)
