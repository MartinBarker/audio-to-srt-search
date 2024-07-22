import os
import re
import argparse
import subprocess
from algoliasearch.search_client import SearchClient
from datetime import timedelta, datetime
import srt
from dotenv import load_dotenv
import json

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

UPLOAD_HISTORY_FILE = 'upload_history.json'

def load_upload_history():
    if os.path.exists(UPLOAD_HISTORY_FILE):
        with open(UPLOAD_HISTORY_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_upload_history(history):
    with open(UPLOAD_HISTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4)

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
    
    return srt_objects, len(srt_objects)

def upload_to_algolia(srt_objects):
    res = index.save_objects(srt_objects, {'autoGenerateObjectIDIfNotExist': True})
    print("Added items.")
    print(res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload all SRT files in a folder to Algolia")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing SRT files")
    args = parser.parse_args()

    upload_history = load_upload_history()
    
    srt_files = [os.path.join(args.folder_path, f) for f in os.listdir(args.folder_path) if f.endswith('.srt')]
    for srt_file in srt_files:
        if srt_file in upload_history:
            print(f"File already uploaded: {srt_file}")
            continue
        
        print(f"Processing file: {srt_file}")
        try:
            srt_objects, quote_count = parse_srt_file(srt_file)
            upload_to_algolia(srt_objects)
            
            # Update the upload history
            file_info = {
                'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'file_size': os.path.getsize(srt_file),
                'quote_count': quote_count
            }
            upload_history[srt_file] = file_info
            save_upload_history(upload_history)
            
        except Exception as e:
            print(f"Error processing file {srt_file}: {e}")
