import os

from datetime import datetime
from instagram_scrapper import InstagramScrapper
from settings import Settings
from thumbnail_scrapper import ThumbnailScrapper
from title_manager import TitleManager
from video_builder_ffmpeg import VideoBuilderFfmpeg
from video_builder_moviepy import VideoBuilderMoviePy
from youtube import YoutubeController
from utils import timeit


# TODO: add some kind of water mark and intro video
# TODO: add dates to settings
# TODO: change the script so the scrape date can be choosen or the scrapper
#       scrapes from the last 24 hours
# TODO: do not print response in youtube module, instead do something else with it
# TODO: create the folders, in remote repo, where the stuff gets scrapped (investigate if necessary or not)
# TODO: put stuff in try catch (calls to api and other stuff that can fail)
# TODO: make CLI

settings = Settings()

@timeit("Scrapping videos took ")
def scrapping():
    print("Started scrapping...")
    insta = InstagramScrapper()

    # iterating over sources and downloading videos
    for source in settings.get_sources():
        user = source.strip("\n ")
        @timeit(f"Scrapping {source}")
        def tmp():
            videos = insta.get_videos_from_interval(user, datetime(2023, 7, 20), datetime.now())
            insta.download_videos(videos, "archive", user)
        tmp()

@timeit("Building video with ffmpeg took ")
def building_video_ffmpeg():
    print("Started building video...")
    builder = VideoBuilderFfmpeg()
    
    builder.concat_videos_from_folder(
        folder_path=settings.get_archive_path(),
        target_path=settings.get_result_path(),
        result_name=settings.get_result_name(),
        duration=settings.get_duration(),
        quiet=True
    )

@timeit("Building video with moviepy took ")
def building_video_moviepy():
    print("Started building video...")
    builder = VideoBuilderMoviePy()

    # Pull videos from folder and resize them
    videos = builder.get_videos_from_folder(settings.get_archive_path(), 1920, 1080)

    # Shuffle videos
    builder.shuffle_videos(videos)

    # Take the first ten minutes of videos
    choosen_videos = []
    duration = 0
    for video in videos:
        duration += video.duration
        choosen_videos.append(video)
        if duration >= settings.get_duration():
            break

    # Build the final video from the choosen videos
    builder.concat_videos(choosen_videos, "./results/result3.mp4")

@timeit("Uploading the video took ")
def upload_video():
    print("Starting uploading video...")
    youtube = YoutubeController()
    thumbnails = ThumbnailScrapper()
    titles = TitleManager(settings, youtube)

    thumbnail_path = thumbnails.choose_random_thumbnail()
    title = titles.choose_random_title()

    youtube.upload_video(
        os.path.join(settings.get_result_path(), settings.get_result_name()),
        thumbnail_path,
        title,
        settings.get_description(),
        settings.get_tags()
    )

@timeit("Everything took ")
def app():
    scrapping()
    building_video_ffmpeg()
    upload_video()

if __name__ == "__main__":
    app()