#!/bin/bash
set -euo pipefail

GIF_PATH="$1"
ANIMATION_NAME="$2"

convert "$GIF_PATH" -coalesce -resize 1000x240 -gravity Center -crop "240x240+0+0" -quality 10 -type TrueColor "${ANIMATION_NAME}%02d.jpg"
