# -*- coding: UTF-8 -*-
from __future__ import print_function
import time
from os import listdir, path 
from utils import show_time, show_info, gen_path_tools, gen_extend_path, ext_pattern, get_ext, val_to_utf8_str, to_utf8_str, filter_media, check_dirs, get_yaml_path, read_yaml
from extract_subtitles import extract_subtitles

def extract_subtitles_batch(data):
  for settings in data:
    val_to_utf8_str(settings, ['input_dir', 'output_dir'])
    check_dirs(settings)
    input_lang = 'zh-TW'
    output_lang = 'zh-TW'
    extension = 'vtt'
    if 'input_lang' in settings: input_lang = to_utf8_str(settings['input_lang'])
    if 'output_lang' in settings: output_lang = to_utf8_str(settings['output_lang'])
    if 'extension' in settings: extension = to_utf8_str(settings['extension'])
    get_it_path, get_ot_path = gen_path_tools(settings, ['input_dir', 'output_dir'])
    input_names = filter(filter_media, listdir(settings['input_dir']))
    input_paths = map(get_it_path, input_names)
    output_paths = map(get_ot_path, input_names)
    output_paths = map(gen_extend_path('-', extension), output_paths)
    final_settings = []
    for i in range(len(input_names)):
      final_settings.append({
        'input_path': input_paths[i],
        'output_path': output_paths[i],
        'input_lang': input_lang,
        'output_lang': output_lang,
        'extension': extension,
      })
    show_info('Input', settings['input_dir'])
    start = time.time()
    extract_subtitles(final_settings)
    show_time(start)
    show_info('Input', settings['input_dir'], is_end=True)

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
        # input_lang: zh-TW
        # output_lang: zh-TW
        # extension: vtt # output extension format
      - input_dir: input_videos_2
        output_dir: output_videos_2
        # input_lang: zh-TW
        # output_lang: zh-TW
        # extension: vtt # output extension format
      ...
      ```
    * Step 2. Run the command
      ```
      $ pipenv run python extract_subtitles_batch.py my_settings.yaml
      ```
    If you don't provide a yaml file and then run the command like this:
    ```
    $ pipenv run python extract_subtitles_batch.py
    ```
    "extract_subtitles_batch.py" would automatically use "extract_subtitles_batch.yaml" as default;
    if "extract_subtitles_batch.yaml" does not exist, the program would raise error.
  """
  yaml_path = get_yaml_path('extract_subtitles_batch.yaml')
  config = read_yaml(yaml_path)
  global_start = time.time()
  extract_subtitles_batch(config['data'])
  show_time(global_start, prefix='Total')

if __name__ == '__main__':
  main()
