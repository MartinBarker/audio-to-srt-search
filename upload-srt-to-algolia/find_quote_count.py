import os
import re
import argparse
import subprocess
from datetime import timedelta
import srt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    
    return len(srt_objects)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count quotes in all SRT files in a folder")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing SRT files")
    args = parser.parse_args()

    total_quotes = 0
    
    srt_files = [os.path.join(args.folder_path, f) for f in os.listdir(args.folder_path) if f.endswith('.srt')]
    for srt_file in srt_files:
        print(f"Processing file: {srt_file}")
        try:
            quote_count = parse_srt_file(srt_file)
            total_quotes += quote_count
            print(f"Quotes in {srt_file}: {quote_count}")
        except Exception as e:
            print(f"Error processing file {srt_file}: {e}")
        print(f"Total quotes in all files: {total_quotes}")

    print(f"Final total quotes in all files: {total_quotes}")
