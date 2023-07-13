import json
import os
from random import shuffle
import subprocess
from utils import cleanup

class VideoBuilderFfmpeg:

    """ VideoBuilderFfmpeg class provides an interface for building videos using ffmpeg. """

    def __init__(self) -> None:
        pass

    def get_duration(self, file_path: str):
        """
            Gets the duration in seconds of the provided file. 
            The file must be a video, otherwise it will result in a runtime error.
        """
        out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", file_path])
        ffprobe_data = json.loads(out)
        duration_seconds = float(ffprobe_data["format"]["duration"])
        return float(duration_seconds)

    def concat_videos_from_folder(
        self, 
        folder_path: str, 
        target_path: str, 
        result_name: str = "out.mp4", 
        duration: int = 3 * 60, 
        quiet: bool = True, 
        width: int = -2, 
        height: int = 1080
        ):
        """
            Takes videos from 'folder_path', resizes them, stores them temporarly, 
            shuffles the videos, takes the wanted 'duration' in videos then it concatenated those
            videos and stores the result in 'target_path/result_name'.
        """
        # set the output, if quiet true nothing will be printed from the ffmpeg command
        stdout = subprocess.DEVNULL if quiet else None

        # create 'tmp' folder if it does not exist
        if not os.path.exists("./tmp"):
            os.mkdir("tmp")
        
        # delete everything from 'tmp' if it exists
        cleanup("./tmp")

        # resize and store all resized videos in 'tmp'
        for path in os.listdir(folder_path):
            if path.endswith(".mp4"):
                subprocess.run(["ffmpeg", "-i", os.path.join(folder_path, path), "-vf", f"scale={width}:{height}", os.path.join("tmp", path)], stderr=stdout)
        
        # take all filenames from 'tmp'
        videos = [path for path in os.listdir(folder_path)]

        # shuffle the videos
        shuffle(videos)

        # take the first videos that add up to the wanted duration
        count = 0
        choosen_videos = []
        for video in videos:
            count += self.get_duration(os.path.join("tmp", video))
            choosen_videos.append(video)
            if count >= duration:
                break

        # create input file for ffmpeg ('list.txt' in this case)
        with open("./tmp/list.txt", "w") as f:
            for video in choosen_videos:
                f.write(f"file '{video}'\n")

        # concat videos specified in the file
        subprocess.run(["ffmpeg", "-f", "concat", "-i", "tmp/list.txt", "-c", "copy", os.path.join(target_path, result_name)], stderr=stdout)

        # clean up 'tmp'
        cleanup("./tmp")

if __name__ == "__main__":
    video_builder = VideoBuilderFfmpeg()
    video_builder.concat_videos_from_folder("./archive", "./results", "out2.mp4", duration=3 * 60, quiet=True)