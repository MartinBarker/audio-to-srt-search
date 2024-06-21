# Convert audio to srt:
- `cd BATCH-FOLDER-AUDIO-TO-SRT`
- Run: `python3 audio-to-srt.py "/mnt/c/filepath/to/audio.m4a"` to convert .m4a audio to srt file.
- .srt file will be outputted to ./SrtFiles in same location where you ran the script.

# Batch convert all audio files in folder to srt:
- `cd BATCH-FOLDER-AUDIO-TO-SRT`
- Run: `python3 run-for-folder.py`
- Input folder hardcoded in script.
- .srt file will be outputted to ./SrtFiles in same location where you ran the script.

# Upload single srt file to algolia database
- cd `upload-srt-to-algolia`
- Fill out `.env` file based off `.env-template`
- Run `python3 test.py` to test out connection.
- Run `python3 upload-srt-to-algolia.py "/mnt/c/Users/marti/My Cool Title [htUDG4re1u4]_subtitles.srt"` to convert .srt file to json and upload to algolia DB.

---------------------------------------------
# Benchmarks
- new-auth-to-srt-fast
    - run with `python3 convert.py "/mnt/d/Jerma985 Streams Audio/Livestream： TF2⧸CS：GO： April 14, 2012 (Pre Recorded) - Jerma985.m4a"`
    - "Livestream： TF2⧸CS：GO： April 14, 2012 (Pre Recorded) - Jerma985.m4a" = 1:18:43 long
    - Took 18:27 to generate srt file.
    - For every minute of input audio, the script processes it in approximately 14.07 seconds.
    - So the 01:58:14 audio file (60+58=118 minutes total) "TF2⧸Tribes： Ascend Livestream! (Pre Recorded) [3qWKO3LVCxc].m4a" should take 118minutes*14.07 = 1660.26 seconds, which is 27.671 minutes.
    - `python3 convert.py "/mnt/d/Jerma985 Streams Audio/TF2⧸Tribes： Ascend Livestream! (Pre Recorded) [3qWKO3LVCxc].m4a"`


# How to setup/use virt env
Windows: `venv_name\Scripts\activate`
Mac/Linux: `source venv_name/bin/activate`
Leave: `deactivate`
`pip freeze > requirements.txt`
`pip install -r requirements.txt`

# Test 1
- `python aaiTest.py > output.txt`

# Test 2
- `python whisperx_example.py`
----------------------------------
https://www.youtube.com/watch?v=SAIsk0i7KgU&t=474s&ab_channel=PromptEngineering

# Convert youtube to mp3
`yt-dlp -f bestaudio -x --audio-format mp3 --audio-quality 0 --add-metadata https://www.youtube.com/watch?v=AL2IkW4JWl4`

# Convert mp3 to txt tracnscript 
https://github.com/openai/whisper
`pip install -U openai-whisper`
`sudo apt update && sudo apt install ffmpeg`
`whisper audio.mp3 --model medium`
`python3 -m whisper jerma\ GROWLS\ at\ chat\ and\ has\ a\ meltdown\ \[AL2IkW4JWl4\].mp3 --model medium`

# Convert audio to transcript with speaker identification
`python aaiTest.py > output.txt`

# WhisperX Diarisation
- https://github.com/m-bain/whisperX
1. Install Conda win10: https://docs.conda.io/projects/miniconda/en/latest/
2. Init conda.exe: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html
3. Follow steps: https://github.com/m-bain/whisperX?tab=readme-ov-file#1-create-python310-environment
4. make sure ffmpeg works from command line
ex: compute_type="int8"
