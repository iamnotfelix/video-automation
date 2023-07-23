import random
from settings import Settings

from youtube import YoutubeController


class TitleManager:
    """ TitleManager class provides a way to manage titles. """

    def __init__(self, settings: Settings, youtube: YoutubeController) -> None:
        self.settings = settings
        self.youtube = youtube

    def delete_title(self, title: str) -> bool:
        titles = self.settings.get_titles()
        if title in titles:
            titles.remove(title)
            self.settings.set_titles(titles)
            self.settings.save()
            return True
        
        return False
    
    def add_titles(self, new_titles: list[str]) -> None:
        titles = self.settings.get_titles()
        for title in new_titles:
            if not title in titles:
                titles.append(title)
        
        self.settings.set_titles(titles)
        self.settings.save()

    def get_all(self) -> list[str]:
        self.settings.get_titles()

    def choose_random_title(self) -> str:
        return random.choice(self.settings.get_titles())


if __name__ == "__main__":
    settings = Settings("test.json")
    youtube = YoutubeController()
    title_manager = TitleManager(settings=settings, youtube=youtube)
    print(title_manager.choose_random_title())
    # title_manager.add_titles(["asdf"])
    # title_manager.add_titles(["asdf", "hjkl"])
    # title_manager.add_titles(["to_delete"])
    # title_manager.delete_title("to_delete")
