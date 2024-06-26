# -*- coding: utf-8 -*-
"""WhisperX_Speaker_Diarization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IHum-j2AOjVOs_ZoqJ5yBUjf1kI4SLmt
"""

!pip install --q git+https://github.com/m-bain/whisperx.git

import whisperx
import gc

device = "cuda"
batch_size = 4 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

audio_file = "sam_altman_lex_podcast_367_short.wav"

audio = whisperx.load_audio(audio_file)

model = whisperx.load_model("large-v2", device, compute_type=compute_type)

result = model.transcribe(audio, batch_size=batch_size)
print(result["segments"]) # before alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

result

diarize_model = whisperx.DiarizationPipeline(use_auth_token="HUGGINGFACE_TOKEN",
                                             device=device)

diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)

diarize_segments

diarize_segments.speaker.unique()









result = whisperx.assign_word_speakers(diarize_segments, result)
print(diarize_segments)
print(result["segments"]) # segments are now assigned speaker IDs

result

