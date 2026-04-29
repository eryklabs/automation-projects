from faster_whisper import WhisperModel
import sys

# adding help message in case I forget the audio filename and forget how to use this script in the future:
if len(sys.argv) < 2:
    print("Usage: python trascribe_v2.py <audio_file> [model_size] [device]")
    print(" model_size: tiny, base, small, medium, large-ve (default: large-v3)")
    print("  device: cuda or cpu (default: cuda)")
    sys.exit(1)

audio_file = sys.argv[1]
model_size = sys.argv[2] if len(sys.argv) > 2 else "large-v3"
device = sys.argv[3] if len(sys.argv) > 3 else "cuda"

output_file = audio_file.rsplit(".", 1)[0] + "_transcript.txt"

# Use "medium" for good quality. "large-v3" if you have a GPU and want best quality.
# "small" or "base" if CPU-only and you want speed over accuracy.
# you can do `python transcribe.py audio.m4a small cpu` to test the small model on CPU, or just `python transcribe.py audio.m4a` to use defaults.
compute_type = "float16" if device == "cuda" else "int8"
model = WhisperModel(model_size, device=device, compute_type=compute_type)

segments, info = model.transcribe(audio_file, beam_size=5)

print(f"Detected language: {info.language} (confidence: {info.language_probability:.2f})")

with open(output_file, "w", encoding="utf-8") as f:
    for segment in segments:
        line = f"[{segment.start:.1f}s -> {segment.end:.1f}s] {segment.text}"
        print(line)
        f.write(line + "\n")

print(f"\nTranscript saved to: {output_file}")