# -*- coding: UTF-8 -*-
from __future__ import print_function
from os import path
import subprocess, time
from utils import show_time, show_info, get_main, get_ext, val_to_utf8_str, check_dirs, get_yaml_path, read_yaml

def get_output_path(output_dir, input_name, idx, x):
  main = get_main(input_name)
  ext = get_ext(input_name)
  start = str(x['start_time']).replace('.', 'p')
  end = str(x['end_time']).replace('.', 'p')
  output_name = '{}_{}_{}_to_{}{}'.format(main, idx, start, end, ext)
  return path.join(output_dir, output_name)

def gen_subclip(input_dir, output_dir, input_name, intervals):
  input_path = path.join(input_dir, input_name)
  for idx, x in enumerate(intervals):
    output_path = get_output_path(output_dir, input_name, idx, x)
    cmd = ['pipenv', 'run', 'python', 'cut.py']
    args = [input_path, str(x['start_time']), str(x['end_time']), output_path]
    show_info('', output_path, level=2)
    st_time = time.time()
    subprocess.call(cmd + args)
    show_time(st_time)
    show_info('', output_path, is_end=True, level=2)

def build_subclips(settings):
  for comb in settings['combnations']:
    val_to_utf8_str(comb, ['input_name'])
    gen_subclip(settings['input_dir'], settings['output_dir'], comb['input_name'], comb['intervals'])

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
        combnations:
        - input_name: 1-final-a.mp4
          intervals:
          - start_time: 0.50
            end_time: 1.56
          - start_time: 1.00
            end_time: 2.00
        - input_name: 2-final-a.mp4
          intervals:
          - start_time: 0.50
            end_time: 1.56
          - start_time: 1.00
            end_time: 2.00
      - input_dir: input_videos_2
        output_dir: output_videos_2
        combnations:
        - input_name: 1-final-b.mp4
          intervals:
          - start_time: 0.50
            end_time: 1.56
          - start_time: 1.00
            end_time: 2.00
        - input_name: 2-final-b.mp4
          intervals:
          - start_time: 0.50
            end_time: 1.56
          - start_time: 1.00
            end_time: 2.00
      ...
      ```
    * Step 2. Run the command
      ```
      $ pipenv run python cut_batch.py my_settings.yaml
      ```
    If you don't provide a yaml file and then run the command like this:
    ```
    $ pipenv run python cut_batch.py
    ```
    "cut_batch.py" would automatically use "cut_batch.yaml" as default;
    if "cut_batch.yaml" does not exist, the program would raise error.
  """
  yaml_path = get_yaml_path('cut_batch.yaml')
  config = read_yaml(yaml_path)
  global_start = time.time()
  for settings in config['data']:
    val_to_utf8_str(settings, ['input_dir', 'output_dir'])
    check_dirs(settings)
    show_info('Input', settings['input_dir'])
    build_subclips(settings)
    show_info('Input', settings['input_dir'], is_end=True)
  show_time(global_start, prefix='Total')

if __name__ == '__main__':
  main()

