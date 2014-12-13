#!/bin/bash
# runs tetris-game

pathname="$(dirname "$0")"

cd "$pathname/all/"

if [[ ! $(which python2) ]]; then
  echo "Please install python2."
  exit 1
fi

exec python2 tetris.py
