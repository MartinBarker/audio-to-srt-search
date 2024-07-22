import os
import subprocess

# Define the input and output folder locations
inputFolder = "/mnt/y/Jerma985 Streams Audio"
outputFolder = "./SrtFiles"

# Function to get the creation time of a file
def get_creation_time(file_path):
    return os.path.getctime(file_path)

# Get a list of all .m4a audio files in the input folder
audio_files = [os.path.join(inputFolder, f) for f in os.listdir(inputFolder) if f.endswith('.m4a') and os.path.isfile(os.path.join(inputFolder, f))]

# Sort the audio files by their creation time (most recent first)
audio_files.sort(key=get_creation_time, reverse=False)  # CHANGE REVERSE=FALSE FOR OLDEST FIRST ORDER

# Iterate through each audio file and call the audio-to-srt.py script
for audio_file in audio_files:
    srt_file_name = os.path.splitext(os.path.basename(audio_file))[0] + "_subtitles.srt"
    srt_file_path = os.path.join(outputFolder, srt_file_name)

    print(f"\nChecking for existing SRT file: {srt_file_path}")
    if os.path.exists(srt_file_path):
        print(f"Skipping {audio_file} as SRT file already exists: {srt_file_path}")
        continue

    print(f"No existing SRT file found for: {audio_file}, proceeding with conversion")

    try:
        result = subprocess.run(['python', 'audio-to-srt.py', audio_file], capture_output=True, text=True, check=True)
        print(f"Successfully processed: {audio_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {audio_file}: {e.stderr}")
