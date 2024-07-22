import os
import re
import argparse
import subprocess
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

print(f"Using Algolia App ID: {ALGOLIA_APP_ID}")
print(f"Using Algolia API Key: {ALGOLIA_API_KEY}")
print(f"Using Algolia Index Name: {ALGOLIA_INDEX_NAME}")

client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)

def get_upload_date(video_id):
    try:
        result = subprocess.run(['yt-dlp', '--print', 'upload_date', f'https://www.youtube.com/watch?v={video_id}'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error fetching upload date for video ID {video_id}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception occurred while fetching upload date for video ID {video_id}: {e}")
        return None

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

    # Fetch the upload date
    upload_date = get_upload_date(video_id)
    if not upload_date:
        upload_date = "Unknown"  # Fallback in case of an error
    print("upload_date = ", upload_date)
    for subtitle in subtitles:
        start = int(subtitle.start.total_seconds())
        duration = int((subtitle.end - subtitle.start).total_seconds())
        quote = subtitle.content.replace('\n', ' ')

        srt_object = {
            'quote': quote,
            'start': start,
            'duration': duration,
            'video_id': video_id,
            'video_title': video_title,
            'upload_date': upload_date  # Add the upload date to the object
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
