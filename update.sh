#!/bin/bash

BLOG_BASE="/var/www/blog.sileht.net/"

if [ "$(hostname -s)" != "alien" ]; then
    ssh root@alien "$BLOG_BASE/contents/$(basename $0)" "$@"
else
    if [ "$USER" != "root" ]; then
        sudo -i "$BLOG_BASE/contents/$(basename $0)" "$@"
    else
        source $BLOG_BASE/venv/bin/activate
        pelican -s $BLOG_BASE/contents/settings.py "$@"
        cp -f $BLOG_BASE/contents/keybase.txt $BLOG_BASE/output/keybase.txt
    fi
fi
