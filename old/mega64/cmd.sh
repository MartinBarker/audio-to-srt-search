#!/bin/bash

yt-dlp --download-archive downloaded.txt --no-post-overwrites -ciwx -f bestaudio --extract-audio --audio-format mp3 --audio-quality 9 --output "%(title)s - %(uploader)s - %(id)s.%(ext)s" --write-thumbnail https://www.youtube.com/watch?v=VpSGkMESkwI&list=PL6roEk_7wxVrD0Cdvg7mKbN7mDh_1BviV
