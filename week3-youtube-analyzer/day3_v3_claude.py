import subprocess
import sys
import whisper
import glob
import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

url = sys.argv[1]

# step 1: download audio
print("[1/3] Downloading audio...")
subprocess.run([
    "yt-dlp", "-x", "--audio-format", "mp3",
    "-o", "%(title)s.%(ext)s", url
])

# step 2: transcribe
mp3_files = glob.glob("*.mp3")
if not mp3_files:
    print("No mp3 file found")
    sys.exit(1)

audio_file = mp3_files[-1]
print(f"\n[2/3] Transcribing: {audio_file}")
start = time.time()
model = whisper.load_model("large-v3")
result = model.transcribe(audio_file)
transcript = result["text"]
elapsed = time.time() - start
print(f"[2/3] Transcription complete. ({elapsed:.0f} seconds)")

# save transcript
transcript_file = audio_file.replace(".mp3", "_transcript.txt")
with open(transcript_file, "w", encoding="utf-8") as f:
    f.write(transcript)

# step 3: analyze with Claude
print(f"\n[3/3] Analyzing with Claude...")
start = time.time()

prompt = f"""You are an expert financial analyst. Analyze this investing video transcript in thorough detail.

1. SUMMARY (3-5 sentences covering the main thesis)
2. EVERY STOCK, ASSET AND COMPANY MENTIONED (include ticker symbol, and what was said about each one — bullish or bearish, and why)
3. ALL KEY POINTS AND INSIGHTS (do not skip anything interesting or notable. List every distinct point the speaker makes, even minor ones. I want comprehensive coverage, not a high-level summary)
4. ACTIONABLE TAKEAWAYS (what should an investor do based on this information?)
5. ALL TOPICS TOUCHED UPON (list all topics, their conclusions, and any interesting notes)
6. CYCLES: What cycles are mentioned? Include specific dates and timeframes.
7. SENTIMENT (bullish/bearish/neutral for each sector or stock discussed)

Be thorough. Do not omit details. I would rather have too much information than too little.

Transcript:
{transcript}
"""

response = requests.post("https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": ANTHROPIC_API_KEY,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    },
    json={
        "model": "claude-sonnet-4-6",
        "max_tokens": 8000,
        "messages": [{"role": "user", "content": prompt}]
    }
)

result = response.json()

# debug: print the response if there's an error
if "content" not in result:
    print("API Error:")
    print(json.dumps(result, indent=2))
    sys.exit(1)

full_response = result["content"][0]["text"]
elapsed = time.time() - start
print(f"[3/3] Analysis complete. ({elapsed:.0f} seconds)")

# save analysis
analysis_file = audio_file.replace(".mp3", "_analysis.txt")
with open(analysis_file, "w", encoding="utf-8") as f:
    f.write(full_response)

print(f"\n{'='*50}")
print("ANALYSIS")
print(f"{'='*50}")
print(full_response)
print(f"\nTranscript: {transcript_file}")
print(f"Analysis: {analysis_file}")