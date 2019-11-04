# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys
from os import path 
from utils import val_to_utf8_str, read_yaml, is_yaml

def concatenate(input_paths, output_path):
  from moviepy.editor import VideoFileClip, concatenate_videoclips
  videos = map(lambda x: VideoFileClip(x), input_paths)
  res = concatenate_videoclips(videos)
  res.write_videofile(output_path, audio_codec='aac', audio_bitrate='3000k')
  # 一定要有audio_codec='aac', 否則會沒聲音

def main():
  """
  # Examples to run this script
  ## Example 1: feed arguments from a yaml/yml file
    * Step 1. Edit your yaml file, 
      ```
      $ vim my_settings.yaml
      ```
      The following is the yaml/yml file example
      ```
      ---
      input_paths:
      - input_videos/螢幕錄製 2019-11-27 上午1.32.10.mov
      - input_videos/螢幕錄製 2019-11-27 上午1.32.19.mov
      - input_videos/螢幕錄製 2019-11-27 上午1.32.27.mov
      output_path: output_videos/test-4.mp4
      ...
      ```
    * Step 2. Run the command
      ```
      $ pipenv run python concatenate.py my_settings.yaml
      ```
  ## Example 2: feed arguments from the command line
    The last argument is the output file path.
    ```
    $ pipenv run python concatenate.py input-1.mp4 input-2.mp4 input-3.mp4 my-output.mp4
    ```
  """
  # The number of arguments here does not include python script itself.
  # The 1st argument is the argument immediately after python script (sys.argv[0]).
  # The 2nd argument is the argument immediately after the 1st argument, and so on.
  input_paths = []
  output_path = ''
  if len(sys.argv) < 2:
    raise ValueError('Please provide at least one argument.')
  if is_yaml(sys.argv[1]):
    # If the 1st argument is yaml file, then neglect the other arguments. 
    # Use yaml as settings.
    settings = read_yaml(sys.argv[1])
    val_to_utf8_str(settings, ['input_paths', 'output_path'], { 'input_paths' })
    input_paths = settings['input_paths']
    output_path = settings['output_path']
  elif len(sys.argv) > 2:
    # If the 1st argument is not yaml file, and the number of arguments is at least 2 
    # this means the last argument is the output file path, and others are input file path.
    for i in range(1, len(sys.argv) - 1):
      input_paths.append(sys.argv[i])
    output_path = sys.argv[-1]
  else:
    # the 1st argument is not yaml file and the number of argument is 1
    raise ValueError(
      'Please provide at least one input file path on the 1st argument and one output file path on the last argument.'
    )
  if path.isfile(output_path):
    raise ValueError('The output file "{}" existed. Please use different output file path.'.format(output_path))
  concatenate(input_paths, output_path)

if __name__ == '__main__':
  main()
