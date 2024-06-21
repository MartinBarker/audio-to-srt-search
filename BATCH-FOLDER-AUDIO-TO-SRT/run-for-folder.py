import os
import subprocess
from datetime import datetime

# Define the input and output folder locations
inputFolder = "/mnt/d/Jerma985 Streams Audio"
outputFolder = "./SrtFiles"  # Assuming this is where the SRT files are stored

# Function to get the creation time of a file
def get_creation_time(file_path):
    return os.path.getctime(file_path)

# Get a list of all .m4a audio files in the input folder
audio_files = [os.path.join(inputFolder, f) for f in os.listdir(inputFolder) if f.endswith('.m4a') and os.path.isfile(os.path.join(inputFolder, f))]

# Sort the audio files by their creation time (oldest first)
audio_files.sort(key=get_creation_time)

# Iterate through each audio file and call the audio-to-srt.py script
for audio_file in audio_files:
    srt_file_name = os.path.splitext(os.path.basename(audio_file))[0] + "_subtitles.srt"
    srt_file_path = os.path.join(outputFolder, srt_file_name)

    print(f"\nChecking for existing SRT file: {srt_file_path}")
    if os.path.exists(srt_file_path):
        print(f"Skipping {audio_file} as SRT file already exists: {srt_file_path}")
        continue

    print(f"No existing SRT file found for: {audio_file}, proceeding with conversion")
    result = subprocess.run(['python3', 'audio-to-srt.py', audio_file], text=True)
    if result.returncode == 0:
        print(f"Successfully processed: {audio_file}")
    else:
        print(f"Error processing {audio_file}: {result.stderr}")
