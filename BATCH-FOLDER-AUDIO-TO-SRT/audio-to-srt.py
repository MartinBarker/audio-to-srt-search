import os
import whisper
from datetime import timedelta
from time import time, strftime, gmtime
import argparse

def transcribe_audio(path):
    start_time = time()

    # Load Whisper model (cached if already downloaded)
    model = whisper.load_model("base")  # Modify model as needed
    print("Whisper model loaded.")

    # Transcribe audio
    transcription = model.transcribe(audio=path)
    segments = transcription['segments']

    # Ensure output directory exists
    srt_directory = "SrtFiles"
    os.makedirs(srt_directory, exist_ok=True)

    audio_filename = os.path.splitext(os.path.basename(path))[0]
    srt_filename = os.path.join(srt_directory, f"{audio_filename}_subtitles.srt")

    # Generate SRT content
    with open(srt_filename, 'w', encoding='utf-8') as srt_file:
        for segment in segments:
            start_time_str = f"0{timedelta(seconds=int(segment['start']))},000"
            end_time_str = f"0{timedelta(seconds=int(segment['end']))},000"
            text = segment['text'].strip()
            segment_id = segment['id'] + 1
            srt_file.write(f"{segment_id}\n{start_time_str} --> {end_time_str}\n{text}\n\n")

    elapsed_time = time() - start_time
    elapsed_time_str = strftime("%H:%M:%S", gmtime(elapsed_time))
    print(f"SRT file generated in {elapsed_time_str}.")

    return srt_filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio to SRT file.")
    parser.add_argument("audio_filepath", type=str, help="Path to the audio file to be transcribed")
    args = parser.parse_args()

    print("Starting transcription...")
    transcribe_audio(args.audio_filepath)
