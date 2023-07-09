from datetime import datetime
from itertools import dropwhile, takewhile
import time
from instaloader import instaloader as ig
from instaloader import Post

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

        
if __name__ == "__main__":


    insta = InstagramScrapper()

    videos = insta.get_videos_from_interval("succc.exe", datetime(2023, 6, 30), datetime.now())
    insta.download_videos(videos, "archive")