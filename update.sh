#!/bin/bash

BLOG_BASE="/var/www/blog.sileht.net/"

OPTS="$@"

if [ "$USER" != "root" ]; then
    sudo -i "$BLOG_BASE/contents/$(basename $0)" $OPTS
else
    source $BLOG_BASE/venv/bin/activate
    echo pelican -s $BLOG_BASE/contents/settings.py $OPTS
    pelican -s $BLOG_BASE/contents/settings.py $OPTS
    cp -f $BLOG_BASE/contents/keybase.txt $BLOG_BASE/output/keybase.txt
fi
