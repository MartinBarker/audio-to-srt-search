# Audio to SRT Conversion and Algolia Upload Guide

## Audio to SRT Conversion

### Convert a single audio file to SRT:
1. Navigate to the project directory:
   ```
   cd batch-folder-audio-to-srt
   ```
2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   ```
   *For Windows:*
   ```
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install git+https://github.com/openai/whisper.git
   ```
4. Convert an audio file (`.m4a`) to an SRT subtitle file:
   ```
   python3 audio-to-srt.py "/path/to/audio/file.m4a"
   ```
5. The generated `.srt` file will be saved in the `./SrtFiles` directory where the script is executed.

### Batch convert all audio files in a folder to SRT:
1. Navigate to the project directory:
   ```
   cd batch-folder-audio-to-srt
   ```
2. Run the batch conversion script:
   ```
   python3 run-for-folder.py
   ```
   *Note:* The input folder is hardcoded in the script. All SRT files will be saved to the `./SrtFiles` directory.

---

## Upload SRT to Algolia Database

### Upload a single SRT file to Algolia:
1. Use the `.env-template` to create and fill out a `.env` file, including your Algolia write access API key (find it [here](https://dashboard.algolia.com/account/api-keys/all?applicationId=A91VDJYTFI)).
2. Navigate to the `upload-srt-to-algolia` directory:
   ```
   cd upload-srt-to-algolia
   ```
3. Run a connection test:
   ```
   python3 test.py
   ```
4. Upload the SRT file:
   ```
   python3 upload-srt-to-algolia.py "/path/to/subtitles.srt"
   ```

### Upload an entire folder to Algolia:
1. Run the following script to check the number of quotes that would be uploaded:
   ```
   python3 find_quote_count.py "/path/to/srt/folder/"
   ```
2. To upload all SRT files from a folder:
   ```
   python3 upload_folder_to_algolia.py "/path/to/srt/folder/"
   ```

---

## Benchmarks

### Processing Speed Example:
- **File:** "Livestream: TF2/CS:GO: April 14, 2012 (Pre Recorded) - Jerma985.m4a" (Length: 1:18:43)
- **Time Taken:** 18 minutes 27 seconds
- **Processing Speed:** 14.07 seconds per minute of audio

Estimate for processing a longer file:
- **File Length:** 1:58:14 (118 minutes)
- **Estimated Time:** 27.67 minutes
- Example:
   ```
   python3 convert.py "/path/to/long/audiofile.m4a"
   ```

---

## Virtual Environment Setup Guide

### Setting up and using a virtual environment:
1. Activate the environment:
   - **Windows:**
     ```
     venv_name\Scripts\activate
     ```
   - **Mac/Linux:**
     ```
     source venv_name/bin/activate
     ```
2. Deactivate the environment:
   ```
   deactivate
   ```
3. Manage dependencies:
   - Freeze installed dependencies to a file:
     ```
     pip freeze > requirements.txt
     ```
   - Install dependencies from a file:
     ```
     pip install -r requirements.txt
     ```

---

## Convert YouTube to MP3
Download and convert YouTube videos to high-quality MP3:
```
yt-dlp -f bestaudio -x --audio-format mp3 --audio-quality 0 --add-metadata https://www.youtube.com/watch?v=AL2IkW4JWl4
```

---

## Convert MP3 to Text Transcript

1. Install Whisper:
   ```
   pip install -U openai-whisper
   sudo apt update && sudo apt install ffmpeg
   ```
2. Convert MP3 to text:
   ```
   whisper audio.mp3 --model medium
   ```

---

## WhisperX Diarization (Speaker Segmentation)

1. Install [Conda](https://docs.conda.io/projects/miniconda/en/latest/).
2. Initialize Conda: [Getting Started](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).
3. Follow the steps for installing WhisperX: [WhisperX](https://github.com/m-bain/whisperX#1-create-python310-environment).
4. Ensure `ffmpeg` is installed and accessible from the command line.
