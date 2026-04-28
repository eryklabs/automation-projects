import subprocess
import sys
import whisper
import glob
import requests
import json
from datetime import date
import time

url = sys.argv[1]



# step 1: download audio
print("Downloading audio...")
subprocess.run([
    "yt-dlp", "-x", "--audio-format", "mp3", 
    "-o", "%(title)s.%(ext)s", url
])


input("Press Enter to run LLM analysis...")


# step 2: transcribe
mp3_files = glob.glob("*.mp3")
if not mp3_files:
    print("No mp3 file found")
    sys.exit(1)

audio_file = mp3_files[-1]
print(f"\nTranscribing: {audio_file}")
model = whisper.load_model("large-v3")
result = model.transcribe(audio_file)
transcript = result["text"]



# save transcript
transcript_file = audio_file.replace(".mp3", "_transcript.txt")
with open(transcript_file, "w", encoding="utf-8") as f:
    f.write(transcript)



# step 3: summarize with local LLM
print("\nAnalyzing with LLM...")
start = time.time()

prompt = f"""You are an expert financial analyst. Analyze this investing video transcript in thorough detail.

1. SUMMARY (3-5 sentences covering the main thesis)
2. EVERY STOCK, ASSET AND COMPANY MENTIONED (include ticker symbol, and what was said about each one — bullish or bearish, and why)
3. ALL KEY POINTS AND INSIGHTS (do not skip anything interesting or notable. List every distinct point the speaker makes, even minor ones. I want comprehensive coverage, not a high-level summary)
4. ACTIONABLE TAKEAWAYS (what should an investor do based on this information?)
5. ALL TOPICS TOUCHED UPON (list all topics touched upon, their conclusions, and any interesting notes about them)
6. CYCLES: What cycles are mentioned?
7. SENTIMENT (bullish/bearish/neutral for each sector or stock discussed)

Be thorough. Do not omit details. Take your time. I would rather have too much information than too little.

DO NOT MAKE STUFF UP!

Transcript: 
{transcript}
"""

response = requests.post("http://localhost:11434/api/generate", json={
    "model": 'qwen3:14b',                    # "qwen3:32b",
    "prompt": prompt, 
    "stream": False,
    "options": {"temperature": 0.1}                    # Lower temperature = more consistent, less creative. 0.1 is good for factual analysis. Default is around 0.7.
    # "options": {"num_predict": 2048}      # for long videos, you can lower this to 2048 or 1024, to shorten summary
})

raw = response.text
lines = raw.strip().split("\n")
full_response = ""
for line in lines:
    data = json.loads(line)
    if "response" in data:
        full_response += data["response"]

elapsed = time.time() - start
print(f"Analysis complete. Time elapsed: {elapsed:.0f} seconds\n")



# save analysis
analysis_file = audio_file.replace(".mp3", "_analysis.txt")
with open(analysis_file, "w", encoding="utf-8") as f:
    f.write(full_response)

print(f"\n{'='*50}")
print("ANALYIS")
print(f"{'='*50}")
print(full_response)
print(f"\nTranscript saved to: {transcript_file}")
print(f"Analysis saved to: {analysis_file}")
