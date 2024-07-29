#! /bin/bash

lower="0"
higher="100"
if [ $# -eq 2 ]; then
  lower="$1"
  higher="$2"
fi

#echo $higher
python3 /home/bongb/hypothesis/hypothesis-python/src/debug_speed_regression.py $lower $higher

exit $?
