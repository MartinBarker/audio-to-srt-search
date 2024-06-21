import os
import whisper
import warnings
from datetime import timedelta
from time import time, strftime, gmtime
import argparse

def transcribe_audio(path):
    start_time = time()

    # Load Whisper model (it uses cached model if already downloaded)
    model = whisper.load_model("base")  # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    # Ensure the SrtFiles directory exists
    srt_directory = "SrtFiles"
    os.makedirs(srt_directory, exist_ok=True)

    audio_filename = os.path.splitext(os.path.basename(path))[0]
    srt_filename = os.path.join(srt_directory, f"{audio_filename}_subtitles.srt")

    for segment in segments:
        start_time_str = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
        end_time_str = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
        text = segment['text']
        segment_id = segment['id'] + 1
        segment_content = f"{segment_id}\n{start_time_str} --> {end_time_str}\n{text[1:] if text[0] == ' ' else text}\n\n"

        with open(srt_filename, 'a', encoding='utf-8') as srt_file:
            srt_file.write(segment_content)

    end_time = time()
    elapsed_time = end_time - start_time
    elapsed_time_str = strftime("%H:%M:%S", gmtime(elapsed_time))
    print(f"SRT file generated in {elapsed_time_str}.")

    return srt_filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio to SRT file.")
    parser.add_argument("audio_filepath", type=str, help="Path to the audio file to be transcribed")
    args = parser.parse_args()

    print("Transcribing audio")
    transcribe_audio(args.audio_filepath)
