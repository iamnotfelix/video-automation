from datetime import datetime
from itertools import dropwhile, takewhile
import time
from instaloader import instaloader as ig
from instaloader import Post
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import re
import moviepy.video.fx.all as vfx
from random import shuffle

time.sleep(2)

class InstagramScrapper:

    def __init__(self) -> None:
        self.loader = ig.Instaloader(save_metadata=False)

    def get_videos_from_interval(self, username: str, start_date: datetime, end_date: datetime) -> list[Post]:
        posts = ig.Profile.from_username(self.loader.context, username).get_posts()
        posts = list(takewhile(lambda p: p.date >= start_date, dropwhile(lambda p: p.date >= end_date, posts)))
        return posts
    
    
    def download_videos(self, posts: list[Post], target: str) -> None:
        self.loader.download_pictures = False
        self.loader.post_metadata_txt_pattern = ""
        # self.loader.filename_pattern = target
        for post in posts:
            self.loader.download_post(post, target)

    # TODO: fix login

    # def get_followees(self, username: str) -> list[Profile]:
    #     self.login()
    #     return list(ig.Profile.from_username(self.loader, username).get_followees())
    
    # def login(self )-> None:
    #     load_dotenv()
    #     self.loader.login(os.getenv("IG_USERNAME"), os.getenv("IG_PASSWORD")) 
    
class VideoBuilder:
    
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


    insta = InstagramScrapper()

    # videos = insta.get_videos_from_interval("succc.exe", datetime(2023, 6, 30), datetime.now())
    # insta.download_videos(videos, "archive")

    video_builder = VideoBuilder()
    # video_builder.concat_videos_from_folder("./archive", "results/result2.mp4")

    videos = video_builder.get_videos_from_folder("./archive", 1920, 1080)
    video_builder.shuffle_videos(videos)
    videos = videos[:10]
    video_builder.concat_videos(videos, "./results/result2.mp4")

    #(1920, 1080)