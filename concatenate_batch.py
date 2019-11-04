# -*- coding: UTF-8 -*-
from __future__ import print_function
from os import listdir, path 
import os
import sys, time
import subprocess
from utils import show_time, show_info, gen_get_path, val_to_utf8_str, get_ext, filter_video, check_dirs, get_yaml_path, read_yaml

def remove_files_of_input_groups(input_groups):
  for g in input_groups:
    for p in g:
      os.remove(p)

def build_group_videos(input_groups, settings, turn, remove_old=False): # turn is 'a_' or 'b_'
  prefix = path.join(settings['output_dir'], turn)
  new_input_paths = []
  for idx, group in enumerate(input_groups):
    input_paths = map(lambda x: '{}'.format(x), group)
    output_path = '{}{}{}'.format(prefix, idx, get_ext(settings['output_name']))
    cmd = ['pipenv', 'run', 'python', 'concatenate.py']
    show_info('', output_path, level=2)
    subprocess.call(cmd + input_paths + [output_path])
    show_info('', output_path, is_end=True, level=2)
    new_input_paths.append(output_path)
  if remove_old:
    remove_files_of_input_groups(input_groups)
  if len(new_input_paths) == 1:
    os.rename(new_input_paths[0], path.join(settings['output_dir'], settings['output_name']))
    return []
  return gen_groups(new_input_paths, settings['group_items'])

def sort_by_last_modified_time(input_paths):
  return sorted(input_paths, key=lambda x: os.stat(x).st_mtime)

def gen_groups(input_paths, group_items):
  input_groups = []
  count = 0
  for p in input_paths:
    if (count % group_items) == 0:
      input_groups.append([])
    input_groups[-1].append(p)
    count += 1
  return input_groups

def get_input_groups(settings):
  if 'group_items' in settings:
    if not isinstance(settings['group_items'], int):
      raise ValueError('group_items should be an integer.')
    if settings['group_items'] <= 0 or settings['group_items'] >= 8:
      raise ValueError('group_items should be larger than 0 and less than 8.')
  else:
    settings['group_items'] = 6
  val_to_utf8_str(settings, ['input_dir', 'output_dir', 'output_name'])
  check_settings(settings)
  input_paths = []
  get_input_path = gen_get_path(settings['input_dir'])
  if ('input_names' in settings) and isinstance(settings['input_names'], list):
    val_to_utf8_str(settings, ['input_names'], { 'input_names' })
    input_paths = map(get_input_path, settings['input_names'])
  else:
    input_names = filter(filter_video, listdir(settings['input_dir']))
    input_paths = map(get_input_path, input_names)
    input_paths = sort_by_last_modified_time(input_paths)
  return gen_groups(input_paths, settings['group_items'])

def check_settings(settings):
  check_dirs(settings)
  if not settings['output_name']:
    raise ValueError('The output_name in yaml can not be empty.')

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
        output_name: my-output-1.mp4
        # group_items: 6
        # input_names:
        # - a.mp4
        # - b.mp4
      - input_dir: input_videos_2
        output_dir: output_videos_2
        output_name: my-output-2.mp4
        # group_items: 6
        # input_names:
        # - c.mp4
        # - d.mp4
      ...
      ```
    * Step 2. Run the command
      ```
      $ pipenv run python concatenate_batch.py my_settings.yaml
      ```
    If you don't provide a yaml file and then run the command like this:
    ```
    $ pipenv run python concatenate_batch.py
    ```
    "concatenate_batch.py" would automatically use "concatenate_batch.yaml" as default;
    if "concatenate_batch.yaml" does not exist, the program would raise error.
  """
  yaml_path = get_yaml_path('concatenate_batch.yaml')
  config = read_yaml(yaml_path)
  global_start = time.time()
  for settings in config['data']:
    input_groups = get_input_groups(settings) # settings['group_items'] could be changed after this line.
    show_info('', settings['output_name'])
    start = time.time()
    turn = 'a_'
    remove_old = False
    while input_groups:
      input_groups = build_group_videos(input_groups, settings, turn, remove_old)
      turn = 'b_' if turn == 'a_' else 'a_'
      remove_old = True
    show_time(start)
    show_info('', settings['output_name'], is_end=True)
  show_time(global_start, prefix='Total')

if __name__ == '__main__':
  main()
