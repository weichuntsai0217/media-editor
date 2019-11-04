# -*- coding: UTF-8 -*-
import subprocess
from utils import to_utf8_str, get_yaml_path, read_yaml

def extract_subtitles(settings):
  for comb in settings: # comb is combnation
    input_path = to_utf8_str(comb['input_path'])
    input_lang = 'zh-TW'
    output_lang = 'zh-TW'
    extension = 'vtt'
    if 'input_lang' in comb: input_lang = to_utf8_str(comb['input_lang'])
    if 'output_lang' in comb: output_lang = to_utf8_str(comb['output_lang'])
    if 'extension' in comb: extension = to_utf8_str(comb['extension'])
    cmd = ['pipenv', 'run', 'autosub']
    args = [input_path, '-S', input_lang, '-D', output_lang, '-F', extension]
    if 'output_path' in comb: args = args + ['-o', to_utf8_str(comb['output_path'])]
    subprocess.call(cmd + args)

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
      - input_path: input_videos_1/a.mp4
        # output_path: output_videos_1/a.vtt
        # input_lang: zh-TW
        # output_lang: zh-TW
        # extension: vtt # output extension format
      - input_path: input_videos_2/b.mp4
        # output_path: output_videos_2/b.vtt
        # input_lang: zh-TW
        # output_lang: zh-TW
        # extension: vtt # output extension format
      ...
      ```
    * Step 2. Run the command
      ```
      $ pipenv run python extract_subtitles.py my_settings.yaml
      ```
    If you don't provide a yaml file and then run the command like this:
    ```
    $ pipenv run python extract_subtitles.py
    ```
    "extract_subtitles.py" would automatically use "extract_subtitles.yaml" as default;
    if "extract_subtitles.yaml" does not exist, the program would raise error.
  """
  yaml_path = get_yaml_path('extract_subtitles.yaml')
  config = read_yaml(yaml_path)
  extract_subtitles(config['data'])

if __name__ == '__main__':
  main()
