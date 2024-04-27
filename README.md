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
