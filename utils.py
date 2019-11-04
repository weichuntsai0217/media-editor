# -*- coding: UTF-8 -*-
from __future__ import print_function
from os import path 
import sys, re, time
import yaml

allowed_video_extension = { '.ogv', '.mp4', '.avi', '.mov', '.mpeg' } # the allowed video extensions for ffmpeg
allowed_audio_extension = { '.mp3', '.wav' } # the allowed audio extensions for ffmpeg
ext_pattern = r'\.[^.]*$'

def show_time(start, prefix=''):
  seconds = time.time() - start
  mins = int(seconds / 60.)
  rs = seconds % 60
  if prefix:
    print('{} running time = {}min {:.2f}s'.format(prefix, mins, rs))
  else:
    print('Running time = {}min {:.2f}s'.format(mins, rs))

def show_info(data_1, data_2, is_end=False, level=1):
  left = '=====' if level == 1 else '###'
  right = left
  term = 'start'
  if is_end:
    term = 'end'
  else:
    left = '\n' + left
  print('{} {} "{}" {} {}'.format(left, data_1, data_2, term, right))

def gen_extend_path(s, extension):
  """
  Generate a function which replaces the last dot with `s`
  and add `extension` in the tail for a target path.
  """
  def func(target):
    ext = get_ext(target)
    new_str = s + ext[1:]
    return re.sub(ext_pattern, new_str, target) + '.' + extension
  return func

def gen_get_path(target_dir):
  def get_path(file_name):
    return path.join(target_dir, file_name)
  return get_path

def filter_video(input_name):
  return (
    (input_name[-4:] in allowed_video_extension) or
    (input_name[-5:] in allowed_video_extension)
  )

def filter_media(input_name):
  return (
    (input_name[-4:] in allowed_audio_extension) or
    (input_name[-4:] in allowed_video_extension) or
    (input_name[-5:] in allowed_video_extension)
  )

def to_utf8_str(x):
  """
  The data read from read_yaml could be unicode or unexpected int or float.
  This function is to convert x into an str if x is a unicode/int/float object.
  If x is an str, do nothing.
  """
  if isinstance(x, unicode):
    return x.encode('utf-8')
  elif isinstance(x, str):
    return x
  elif isinstance(x, (int, float)):
    return str(x)
  raise ValueError('The input arg should be a unicode/int/float/str object.')

def val_to_utf8_str(dic, keys, is_list_map=None):
  """
  dic is a dict.
  """
  if not is_list_map: is_list_map = {}
  for k in keys:
    if k in is_list_map:
      dic[k] = map(to_utf8_str, dic[k])
    else:
      dic[k] = to_utf8_str(dic[k])

def gen_path_tools(dic, keys):
  res = []
  for k in keys:
    res.append(gen_get_path(dic[k]))
  return res

def get_main(target): # get main file name
  return re.sub(ext_pattern, '', target)

def get_ext(target): # get file extension name
  m = re.search(ext_pattern, target)
  return m.group(0)

def check_dirs(settings):
  if settings['input_dir'] == settings['output_dir']:
    raise ValueError('The input directory and output directory should not be the same.')
  if (not path.isdir(settings['input_dir'])) or (not path.isdir(settings['output_dir'])):
    raise ValueError('The input directory or output directory does not exist.')

def read_yaml(filename):
  settings = None
  with open(filename, 'r') as stream:
    settings = yaml.safe_load(stream)
  if not settings:
    raise ValueError('The content of ' + filename + ' is empty or something wrong in yaml loader.')
  return settings

def get_yaml_path(default_path):
  if (not isinstance(default_path, str)) or (not default_path):
    raise ValueError('default_path can not be empty.')
  target = default_path if len(sys.argv) < 2 else sys.argv[1]
  if target and path.isfile(target) and is_yaml(target):
    return target
  raise ValueError('The input yaml/yml file does not exist.')

def is_yaml(s):
  if isinstance(s, str) and (s.endswith('.yaml') or s.endswith('.yml')):
    return True
  return False
