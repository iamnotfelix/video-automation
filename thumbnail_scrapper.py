import os
import random
from urllib import request
import uuid
from youtube import YoutubeController


class ThumbnailScrapper:
    """ ThumbnailScrapper class provides an interface for scrapping thumbnails from youtube videos. """

    def __init__(self, target_path: str = "thumbnails") -> None:
        
        # if target path does not exist, create it
        if not os.path.exists(target_path) or not os.path.isdir(target_path):
            os.mkdir(target_path)

        self.target_path = target_path
        self.youtube = YoutubeController()

    def get_thumbnails_from_channel(self, channel_id: str, nr: int = 0) -> None:
        video_ids = self.youtube.get_video_ids(channel_id)

        if nr > 0:
            video_ids = video_ids[:nr]

        for video_id in video_ids:
            file_name = str(uuid.uuid4()) + ".jpeg"
            url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            try:
                request.urlretrieve(url, os.path.join(self.target_path, file_name))
            except Exception as e:
                print(e)
                print(video_id, url)

    def get_thumbnail_from_video(self, video_url: str, file_name: str) -> None:
        if len(video_url) == 0:
            return
        
        video_id = video_url.split('?v=')[1]
        url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        try:
            request.urlretrieve(url, os.path.join(self.target_path, file_name))
        except Exception as e:
            print(e)

    def choose_random_thumbnail(self) -> str:
        thumbnails = [file_name for file_name in os.listdir(self.target_path)]
        return os.path.join(self.target_path, random.choice(thumbnails))


if __name__ == "__main__":
    thumbnail_scrapper = ThumbnailScrapper()
    # thumbnail_scrapper.get_thumbnail_from_video("https://www.youtube.com/watch?v=_GqP-qo0h7g", "asdf.jpeg")
    # thumbnail_scrapper.get_thumbnails_from_channel("UCJlxrVg_KbrVJIR3zoUlWxQ")
    # print(thumbnail_scrapper.choose_random_thumbnail())

