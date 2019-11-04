# -*- coding: UTF-8 -*-
import sys
from moviepy.editor import VideoFileClip, AudioFileClip

def extract_audio(input_path, output_path):
  video = VideoFileClip(input_path)
  audio = video.audio
  audio.write_audiofile(output_path)

def main():
  """
  # Examples to run this script
  ## Example 1: feed arguments from the command line
    ```
    $ pipenv run python extract_audio.py input-video.mp4 output-audio.mp3
    ```
  """
  input_path = sys.argv[1]
  output_path = sys.argv[2]
  extract_audio(input_path, output_path)

if __name__ == '__main__':
  main()
