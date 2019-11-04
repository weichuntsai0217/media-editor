# -*- coding: UTF-8 -*-
import sys
from moviepy.editor import VideoFileClip, AudioFileClip

def set_audio(input_video, input_audio, output_video):
  video = VideoFileClip(input_video)
  audio = AudioFileClip(input_audio)
  output = video.set_audio(audio)
  output.write_videofile(output_video, audio_codec='aac', audio_bitrate='3000k')

def main():
  """
  # Examples to run this script
  ## Example 1: feed arguments from the command line
    ```
    $ pipenv run python set_audio.py my_video.mp4 my_audio.mp3 my_output_video.mp4
    ```
    The 1st argument (my_video.mp4) is the input video, the 2nd argument (my_audio.mp3) is the input audio,
    and the 3rd argument (my_output_video.mp4) is the output video path.
  """
  input_video = sys.argv[1]
  input_audio = sys.argv[2]
  output_video = sys.argv[3]
  set_audio(input_video, input_audio, output_video)

if __name__ == '__main__':
  main()
