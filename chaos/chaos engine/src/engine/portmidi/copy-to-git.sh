#!/bin/sh
# copy-to-git.sh -- script to copy from portmidi checkout from svn to
#     RBD's local clone of rbdannenberg/portmidi
#
# changed files are updated; doc/html from Doxygen is moved to docs for
#     Github Pages feature.
#
# run this in /Users/rbd/portmedia/portmidi

# Roger B. Dannenberg
# September 2021

rsync -av ./ /Users/rbd/github-portmidi/portmidi/trunk/
# this created the directory doc, but we want the files elsewhere:
rsync -av doc/html/ /Users/rbd/github-portmidi/docs
rm -rf /Users/rbd/github-portmidi/portmidi/trunk/doc
# don't need .svn files either
rm -rf /Users/rbd/github-portmidi/portmidi/trunk/.svn

