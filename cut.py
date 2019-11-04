# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys

def check_argv(argv):
  if len(argv) < 5:
    raise ValueError('Please provide 4 arguments, that is input_path, start_time, end_time, and output_path')

def cut(input_path, start_time, end_time, output_path):
  from moviepy.editor import VideoFileClip
  video = VideoFileClip(input_path)
  res = video.subclip(start_time, end_time)
  res.write_videofile(output_path, audio_codec='aac')
  '''
  一定要有audio_codec='aac', 否則會沒聲音
  '''

def main():
  """
  # Examples to run this script
  ## Example 1: feed arguments from the command line
    ```
    $ pipenv run python cut.py input.mp4 1.25 3.48 output-subclip.mp4
    ```
  """
  check_argv(sys.argv)
  input_path = sys.argv[1]
  start_time = float(sys.argv[2])
  end_time = float(sys.argv[3])
  output_path = sys.argv[4]
  cut(input_path, start_time, end_time, output_path)

if __name__ == '__main__':
  main()

