import subprocess 
import sys
import whisper

url = sys.argv[1]   # takes the URL from the command line

# download audio
subprocess.run([
    "yt-dlp",
    "-x",                       # extract audio only
    "--audio-format", "mp3",    # convert to mp3
    "-o", "%(title)s.%(ext)s",  # name the file after the video title
    url
])



# find the mp3 file that we just downloaded
import glob
mp3_files = glob.glob("*.mp3")
if not mp3_files:
    print("No mp3 file found")
    sys.exit(1)

audio_file = mp3_files[-1]  # most recent mp3
print(f"\nTranscribing: {audio_file}")



# transcribe
model = whisper.load_model("large-v3", device="cuda")
result = model.transcribe(audio_file)

print(f"\n{'='*50}")
print("TRANSCRIPT")
print(f"{'='*50}")
print(result["text"])



# save transcript to file
transcript_file = audio_file.replace(".mp3", "_transcript.txt")
with open(transcript_file, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"\nSaved to: {transcript_file}")