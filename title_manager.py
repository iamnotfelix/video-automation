import json
import random

from youtube import YoutubeController


class TitleManager:
    """ TitleManager class provides a way to manage titles. """

    def __init__(self, file_path: str = "titles.json") -> None:
        self.file_path = file_path
        self.youtube = YoutubeController()

    def get_titles_from_channel(self, channel_id: str, nr: int = 0) -> None:
        titles = self.youtube.get_video_titles(channel_id)

        if nr > 0:
            titles = titles[:nr]

        data = json.dumps({ "titles" : titles })
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(data)

    def choose_random_title(self) -> str:
        with open(self.file_path, "r") as file:
            data = json.load(file)
            return random.choice(data["titles"])


if __name__ == "__main__":
    title_manager = TitleManager()
    # print(title_manager.choose_random_title())
    title_manager.get_titles_from_channel("UCJlxrVg_KbrVJIR3zoUlWxQ")