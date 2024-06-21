# Fill out .env (use .env-template)
# Run with: python3 upload-srt-to-algolia.py "/mnt/c/Users/marti/Documents/projects/audio-to-srt-search/BATCH-FOLDER-AUDIO-TO-SRT/SrtFiles/Livestream： TF2⧸QWOP： April 21, 2012 (Pre-Recorded) [htUDG4re1u4]_subtitles.srt"

import os
import re
import argparse
from algoliasearch.search_client import SearchClient
from datetime import timedelta
import srt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Algolia search client
ALGOLIA_APP_ID = os.getenv('ALGOLIA_APP_ID')
ALGOLIA_API_KEY = os.getenv('ALGOLIA_API_KEY')
ALGOLIA_INDEX_NAME = os.getenv('ALGOLIA_INDEX_NAME')

client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)

def parse_srt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        subtitles = list(srt.parse(content))

    # Extract the video ID from the last set of brackets
    video_id_match = re.search(r'\[([^\]]+)\]_subtitles\.srt$', os.path.basename(filepath))
    if video_id_match:
        video_id = video_id_match.group(1)
    else:
        raise ValueError("Video ID not found in the filename")

    video_title = re.sub(r'\s*\[([^\]]+)\]_subtitles\.srt$', '', os.path.basename(filepath)).strip()
    srt_objects = []

    for subtitle in subtitles:
        start = int(subtitle.start.total_seconds())
        duration = int((subtitle.end - subtitle.start).total_seconds())
        quote = subtitle.content.replace('\n', ' ')

        srt_object = {
            'quote': quote,
            'start': start,
            'duration': duration,
            'video_id': video_id,
            'video_title': video_title
        }
        srt_objects.append(srt_object)
    
    return srt_objects

def upload_to_algolia(srt_objects):
    res = index.save_objects(srt_objects, {'autoGenerateObjectIDIfNotExist': True})
    print("Added items.")
    print(res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload SRT file to Algolia")
    parser.add_argument("srt_filepath", type=str, help="Path to the SRT file to be uploaded")
    args = parser.parse_args()

    srt_objects = parse_srt_file(args.srt_filepath)
    upload_to_algolia(srt_objects)
