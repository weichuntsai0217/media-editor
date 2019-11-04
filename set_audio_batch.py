# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys, time
import subprocess
from utils import show_time, show_info, gen_path_tools, val_to_utf8_str, check_dirs, get_yaml_path, read_yaml

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
      data:
      - input_dir: input_videos_1
        output_dir: output_videos_1
        combinations:
        - input_video: a.mp4
          input_audio: a.mp3
          output_video: a-final.mp4
        - input_video: b.mp4
          input_audio: b.mp3
          output_video: b-final.mp4
      - input_dir: input_videos_2
        output_dir: output_videos_2
        combinations:
        - input_video: c.mp4
          input_audio: c.mp3
          output_video: c-final.mp4
        - input_video: d.mp4
          input_audio: d.mp3
          output_video: d-final.mp4
      ...
      ```
    * Step 2. Run the command
      ```
      $ pipenv run python set_audio_batch.py my_settings.yaml
      ```
    If you don't provide a yaml file and then run the command like this:
    ```
    $ pipenv run python set_audio_batch.py
    ```
    "set_audio_batch.py" would automatically use "set_audio_batch.yaml" as default;
    if "set_audio_batch.yaml" does not exist, the program would raise error.
  """
  yaml_path = get_yaml_path('set_audio_batch.yaml')
  config = read_yaml(yaml_path)
  global_start = time.time()
  for settings in config['data']:
    val_to_utf8_str(settings, ['input_dir', 'output_dir'])
    check_dirs(settings)
    get_it_path, get_ot_path = gen_path_tools(settings, ['input_dir', 'output_dir'])
    show_info('Input', settings['input_dir'])
    for comb in settings['combinations']:
      val_to_utf8_str(comb, ['input_video', 'input_audio', 'output_video'])
      input_video = get_it_path(comb['input_video'])
      input_audio = get_it_path(comb['input_audio'])
      output_video = get_ot_path(comb['output_video'])
      cmd = ['pipenv', 'run', 'python', 'set_audio.py']
      args = [input_video, input_audio, output_video]
      show_info('', output_video, level=2)
      start = time.time()
      subprocess.call(cmd + args)
      show_time(start)
      show_info('', output_video, is_end=True, level=2)
    show_info('Input', settings['input_dir'], is_end=True)
  show_time(global_start, prefix='Total')

if __name__ == '__main__':
  main()
