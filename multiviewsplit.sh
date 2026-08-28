#!/bin/sh
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/split_mlt_per_file_per_video.py" "$@"