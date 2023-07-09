import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import re
import moviepy.video.fx.all as vfx
from random import shuffle

class VideoBuilderMoviePy:
    
    def __init__(self) -> None:
        pass

    def concat_videos_from_folder(self, folder_path: str, target: str, width: int, height: int) -> None:
        videos: list[VideoFileClip] = []
        mp4 = r"\.mp4$"
        for path in os.listdir(folder_path):
            if re.search(mp4, path):
                video = VideoFileClip(folder_path + "/" + path)
                video = video.fx(vfx.resize, width=width)
                video = video.fx(vfx.resize, height=height)
                videos.append(video)
            
        final_video = concatenate_videoclips(videos, method="compose")
        final_video.write_videofile(target, threads=8)

    def concat_videos(self, videos: list[VideoFileClip], target: str) -> None:
        final_video = concatenate_videoclips(videos, method="compose")
        final_video.write_videofile(target, threads=8)

    def get_videos_from_folder(self, folder_path: str, width: int, height: int) -> list[VideoFileClip]:
        videos: list[VideoFileClip] = []
        mp4 = r"\.mp4$"
        for path in os.listdir(folder_path):
            if re.search(mp4, path):
                video = VideoFileClip(folder_path + "/" + path)
                video = video.fx(vfx.resize, width=width)
                video = video.fx(vfx.resize, height=height)
                videos.append(video)

        return videos

    def shuffle_videos(self, videos: list[VideoFileClip]) -> list[VideoFileClip]:
        shuffle(videos)


if __name__ == "__main__":

    video_builder = VideoBuilderMoviePy()
    # video_builder.concat_videos_from_folder("./archive", "results/result2.mp4")

    videos = video_builder.get_videos_from_folder("./archive", 1920, 1080)
    video_builder.shuffle_videos(videos)
    videos = videos[:10]
    video_builder.concat_videos(videos, "./results/result2.mp4")

    #(1920, 1080)