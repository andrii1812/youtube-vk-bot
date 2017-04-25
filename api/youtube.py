import os
import re

from pytube import YouTube


class YouTubeVideo:
    def __init__(self, path, name):
        self.path = path
        self.name = name


def get_youtube_video(vid_url, max_res):
    yt = YouTube(vid_url)
    videos = yt.get_videos()
    video = None

    for vid in videos:
        if vid.resolution == max_res:
            video = vid

    if not video:
        video = videos[-1]

    return video


def download_youtube_video(folder, video_obj):
    video_obj.download(folder)


def prepare_for_download(path, filename):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        path = os.path.join(path, filename)
        if os.path.exists(path):
            os.remove(path)


def download(vid_url, tmp_path, res='720p'):
    video = get_youtube_video(vid_url, res)
    filename = video.filename + '.' + video.extension

    prepare_for_download(tmp_path, filename)
    download_youtube_video(tmp_path, video)

    return YouTubeVideo(os.path.join(tmp_path, filename), video.filename)


def validate(url):
    return re.match('https?:\/\/((www\.youtube\.com\/watch\?v=)|(youtu\.be\/))[A-z0-9]+', url)

if __name__ == '__main__':
    download("https://www.youtube.com/watch?v=xgTYSsaNU_A", '144p')