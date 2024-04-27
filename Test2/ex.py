import whisperx
import gc

device ="cuda"
batch_size = 32
compute_type = "float16"
audio_file = "MEGA64 PODCAST 483.mp3"
audio = whisperx.load_audio(audio_file)
model = whisperx.load_model("large-v2", device, compute_type=compute_type)
result = model.transcribe(audio, batch_size=batch_size)
print(result["segments"])

model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

# https://huggingface.co/settings/tokens
# new read token
HUGGING_FACE_TOKEN="xxxx"
diarize_model = whisperx.DiarizationPipeline(use_auth_token=HUGGING_FACE_TOKEN, device=device)
diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)
print(diarize_segments)
print(diarize_segments.speaker.unique())
result = whisperx.assign_word_speakers(diarize_segments, result)
print(diarize_segments)
print(result["segments"]) # segments area now assigned speaker IDs 


