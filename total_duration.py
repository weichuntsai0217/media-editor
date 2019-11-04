# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys
from moviepy.editor import VideoFileClip

def get_duration(input_path):
  """
  The output duration is in seconds.
  """
  return VideoFileClip(input_path).duration

def check_argv(argv):
  if len(argv) != 2:
    raise ValueError('Please provide only one argument as the input file path.')

def main():
  """
  # Examples to run this script
  ## Example 1: feed arguments from the command line
    All arguments are directory path.
    ```
    $ pipenv run python total_duration.py input_videos/my-video.mp4
    ```
  """
  check_argv(sys.argv)
  input_path = sys.argv[1]
  seconds = get_duration(input_path)
  print(seconds)

if __name__ == '__main__':
  main()
