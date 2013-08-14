#!/bin/bash
#
# Set the colorscheme to be used for the theme.
#
# This script sets up symbolic links to point to the image files and CSS
# file needed for the given color.
#

if [ $# -ne 1 ]; then
    echo "error: a single argument is required"
    exit 1
fi
color="$1"

destinations=("sphinx13_mod.css"
              "headerbg.png"
              "footerbg.png"
              "relbg.png")

for dest in ${destinations[@]}; do
    target_name="${dest%.*}"
    target_ext="${dest##*.}"
    target="${target_name}-${color}.${target_ext}"
    if [ ! -f $target ]; then
        echo "error: target does not exist '${target}'"
        exit 2
    fi
    if [ -f $dest ]; then
        rm -f $dest
    fi
    cp $target $dest
    echo "cp $target $dest"
done
