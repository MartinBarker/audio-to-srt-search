import os
import re
import argparse
import subprocess
import requests
import srt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Elasticsearch URL (replace with your actual EC2 public IP and port)
ES_HOST = 'http://54.176.113.237:9200'
ES_INDEX = 'quotes'  # Replace with your Elasticsearch index name

def get_upload_date(video_id):
    try:
        result = subprocess.run(['yt-dlp', '--print', 'upload_date', f'https://www.youtube.com/watch?v={video_id}'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error fetching upload date for video ID {video_id}: {result.stderr}")
            return "20200101"  # Default to 2020-01-01 if there's an error
    except Exception as e:
        print(f"Exception occurred while fetching upload date for video ID {video_id}: {e}")
        return "20200101"  # Default to 2020-01-01 in case of an exception

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
    print(f"upload_date = {upload_date}")
    
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
            'upload_date': upload_date,  # Add the upload date to the object
            'objectID': f"{video_id}-{start}"
        }
        srt_objects.append(srt_object)
    
    return srt_objects

def upload_to_elasticsearch(srt_objects):
    headers = {
        'Content-Type': 'application/json'
    }
    for obj in srt_objects:
        url = f"{ES_HOST}/{ES_INDEX}/_doc/{obj['objectID']}?pretty"
        response = requests.post(url, headers=headers, json=obj)
        if response.status_code == 201:
            print(f"Successfully added document {obj['objectID']} to Elasticsearch")
        elif response.status_code == 200 and response.json().get('result') == 'updated':
            print(f"Successfully updated document {obj['objectID']} in Elasticsearch")
        else:
            print(f"Failed to add/update document {obj['objectID']} to Elasticsearch: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload SRT files in a folder to Elasticsearch")
    parser.add_argument("srt_folderpath", type=str, help="Path to the folder containing SRT files to be uploaded")
    args = parser.parse_args()

    # Process each .srt file in the given folder
    for root, dirs, files in os.walk(args.srt_folderpath):
        for file in files:
            if file.endswith(".srt"):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}")
                srt_objects = parse_srt_file(filepath)
                upload_to_elasticsearch(srt_objects)
