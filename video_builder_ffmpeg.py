import ffmpeg
import os

class VideoBuilderFfmpeg:

    def __init__(self) -> None:
        pass

    def concat_videos_from_folder(self, folder_path: str, target: str, width: int = 1920, height: int = 1080):
        if os.path.exists(target):
            os.remove(target)
        
        # videos = [os.path.join(folder_path, path) for path in os.listdir(folder_path)]
        # # videos = videos[:2]

        # for video in videos:
        #     (ffmpeg.input(video)
        #      .filter("scale", width="-1", height=height)
        #      .filter("fps", fps=30)
        #      .output(os.path.join("test", os.path.basename(video)))
        #      .run())
            
        # videos = [os.path.join("test", path) for path in os.listdir("./test")]
        
        reshaped_videos = [ffmpeg.input(os.path.join("test", path)) for path in os.listdir("test")]
        reshaped_videos = reshaped_videos[:2]
        video_and_audio_files = [item for sublist in map(lambda f: [f.video, f.audio], reshaped_videos) for item in sublist]

        joined = (ffmpeg
                  .concat(*video_and_audio_files, v=1))

        print((ffmpeg
         .output(joined, target, format='mp4')
         .run()))

        
        # video_inputs = []
        # audio_inputs = []
        # for video in videos:
        #     input = ffmpeg.input(video)
        #     # input = ffmpeg.filter(input, "scale", width="-1", height=height)

        #     video_input = input.video
        #     audio_input = input.audio

        #     video_inputs.append(video_input)
        #     audio_inputs.append(audio_input)

        # videos_concat = ffmpeg.concat(*video_inputs, v=1, a=0)
        # audios_concat = ffmpeg.concat(*audio_inputs, v=0, a=1)

        # concat = ffmpeg.concat(videos_concat, audios_concat, v=1, a=1)

        # output = ffmpeg.output(concat, target).compile()
        # print(output)


if __name__ == "__main__":
    video_builder = VideoBuilderFfmpeg()
    video_builder.concat_videos_from_folder("./archive", "./results/output2.mp4")