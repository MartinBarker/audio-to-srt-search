#!/bin/bash

yt-dlp --download-archive downloaded.txt \
       --no-post-overwrites \
       -ciwx \
       -f bestaudio[ext=m4a] \
       --extract-audio \
       --audio-format mp3 \
       --audio-quality 9 \
       --output "%(title)s - %(uploader)s.%(ext)s" \
       https://www.youtube.com/watch?v=g_ClrEwRmB8&ab_channel=JermaStreamArchive
