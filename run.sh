#!/bin/bash
# runs tetris-game

pathname="$(dirname "$0")"

cd "$pathname/all/"
python2 tetris.py
