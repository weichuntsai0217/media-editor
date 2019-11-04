#!/bin/bash

script="$1" # concatenate_batch.py
do_only="$2"

main_name=`echo $script | sed 's/\.py$//g'` # concatenate_batch
folder="test_${main_name}" # test_concatenate_batch
default_src="${main_name}_yaml.txt" # concatenate_batch_yaml.txt
default_dst="${main_name}.yaml" # concatenate_batch.yaml
custom_src="${main_name}_custom_yaml.txt" # concatenate_batch_custom_yaml.txt
custom_dst="${main_name}_custom.yaml" # concatenate_batch_custom.yaml

echo '=== Test Info ==='
echo "script is $script"
echo "folder is $folder"
echo "default_src is $default_src"
echo "default_dst is $default_dst"
echo "custom_src is $custom_src"
echo "custom_dst is $custom_dst"
echo ""

if [ -f $default_dst ]; then
  mv $default_dst ${default_dst}.backup.tmp
fi

if [ "$do_only" == '1' ]; then
  cp ${folder}/${default_src} $default_dst
  pipenv run python $script
  rm $default_dst
elif [ "$do_only" == '2' ]; then
  cp ${folder}/${custom_src} $custom_dst
  pipenv run python $script $custom_dst
  rm $custom_dst
else
  cp ${folder}/${default_src} $default_dst
  pipenv run python $script
  rm $default_dst
  cp ${folder}/${custom_src} $custom_dst
  pipenv run python $script $custom_dst
  rm $custom_dst
fi

if [ -e "${default_dst}.backup.tmp" ]; then
  mv ${default_dst}.backup.tmp $default_dst
fi
