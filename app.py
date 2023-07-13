from datetime import datetime
from instagram_scrapper import InstagramScrapper
from video_builder_ffmpeg import VideoBuilderFfmpeg
from video_builder_moviepy import VideoBuilderMoviePy
from utils import timeit


DURATION = 3 * 60               # the length of the result videos in seconds (i.e. 10 * 60 = 600 = 10 minutes)
SOURCE_PATH = "sources.txt"     # path to file containing instagram usernames to scrape from
TARGET_PATH = "./results"       # path to folder where the final videos will be
VIDEOS_PATH = "./archive"       # path to folder where the scrapped videos will end up
USE_FFMPEG = True               # change to False if you want to use moviepy(slower than ffmpeg)
RESULT_NAME = "out3.mp4"        # name of the resulted video


@timeit("Scrapping videos took ")
def scrapping():
    print("Started scrapping...")
    insta = InstagramScrapper()

    # Open text file containing pages to scrape
    with open(SOURCE_PATH, "r") as f:
        lines = f.readlines()
        for line in lines:
            user = line.strip("\n ")
            @timeit(f"Scrapping {line}")
            def tmp():
                videos = insta.get_videos_from_interval(user, datetime(2023, 7, 12), datetime.now())
                insta.download_videos(videos, "archive", user)
            tmp()

@timeit("Building video with ffmpeg took ")
def building_video_ffmpeg():
    print("Started building video...")
    builder = VideoBuilderFfmpeg()
    
    builder.concat_videos_from_folder(
        folder_path=VIDEOS_PATH,
        target_path=TARGET_PATH,
        result_name=RESULT_NAME,
        duration=DURATION,
        quiet=True
    )

@timeit("Building video with moviepy took ")
def building_video_moviepy():
    print("Started building video...")
    builder = VideoBuilderMoviePy()

    # Pull videos from folder and resize them
    videos = builder.get_videos_from_folder(VIDEOS_PATH, 1920, 1080)

    # Shuffle videos
    builder.shuffle_videos(videos)

    # Take the first ten minutes of videos
    choosen_videos = []
    duration = 0
    for video in videos:
        duration += video.duration
        choosen_videos.append(video)
        if duration >= DURATION:
            break

    # Build the final video from the choosen videos
    builder.concat_videos(choosen_videos, "./results/result3.mp4")


if __name__ == "__main__":
    scrapping()
    building_video_ffmpeg()