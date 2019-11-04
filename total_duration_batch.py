# -*- coding: UTF-8 -*-
from __future__ import print_function
from os import listdir, path 
import sys, time, subprocess
from utils import gen_get_path, filter_video

def get_input_paths(input_dir):
  input_names = listdir(input_dir)
  res = filter(filter_video, input_names)
  if res:
    res = map(gen_get_path(input_dir), res)
  return res

def show_total_duration(input_dir, seconds, mins, rs):
  print('\n===== {} total duration ====='.format(input_dir))
  print('{}s = {}min {:.2f}s'.format(seconds, mins, rs))

def get_total_duration(input_paths):
  seconds = 0
  cmd = ['pipenv', 'run', 'python', 'total_duration.py']
  for arg in input_paths:
    seconds += float(subprocess.check_output(cmd + [arg]))
  mins = int(seconds / 60.)
  rs = seconds % 60
  return seconds, mins, rs

def check_argv(argv):
  if len(argv) < 2:
    raise ValueError('Please provide at least one argument as a input irectory on the 1st argument.')
  for i in range(1, len(argv)):
    if not path.isdir(argv[i]):
      n = '{}th'.format(i)
      if i == 1: n = '1st'
      if i == 2: n = '2nd'
      if i == 3: n = '3rd'
      raise ValueError(
        'The directory "{}" in the {} argument does not exist, please provide an existed direcroty.'
        .format(
          argv[i],
          n,
        )
      )

def main():
  """
  # Examples to run this script
  ## Example 1: feed arguments from the command line
    All arguments are directory path.
    ```
    $ pipenv run python total_duration.py input_videos_1/ input_videos_2/
    ```
  """
  check_argv(sys.argv)
  for i in range(1, len(sys.argv)):
    input_dir = sys.argv[i]
    input_paths = get_input_paths(input_dir)
    seconds, mins, rs = get_total_duration(input_paths)
    show_total_duration(input_dir, seconds, mins, rs)

if __name__ == '__main__':
  main()
