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

link_destinations=("sphinx13_mod.css"
                   "headerbg.png"
                   "footerbg.png"
                   "relbg.png")

for link_dest in ${link_destinations[@]}; do
    link_target_name="${link_dest%.*}"
    link_target_ext="${link_dest##*.}"
    link_target="${link_target_name}-${color}.${link_target_ext}"
    if [ ! -f $link_target ]; then
        echo "error: link target does not exist '${link_target}'"
        exit 2
    fi
    if [ -f $link_dest ]; then
        rm -f $link_dest
    fi
    ln -s $link_target $link_dest
    echo "ln -s $link_target $link_dest"
done
