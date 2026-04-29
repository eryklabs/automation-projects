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


# input("Press Enter to run LLM analysis...")


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



def ask_llm(prompt):
    """Send a prompt to Ollama and return the response."""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen3:14b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    })
    raw = response.text
    lines = raw.strip().split("\n")
    full_response = ""
    for line in lines:
        data = json.loads(line)
        if "response" in data:
            full_response += data["response"]
    return full_response



def chunk_text(text, words_per_chunk=800):
    """Split text into chunks of roughly equal word count."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), words_per_chunk):
        chunk = " ".join(words[i:i + words_per_chunk])
        chunks.append(chunk)
    return chunks




# step 3: chunked analysis
print("\nAnalyzing with LLM (chunked)...")
start = time.time()



# split transcript into ~5 minute chunks (~800 words each)
chunks = chunk_text(transcript, words_per_chunk=800)
print(f"    Split into {len(chunks)} chunks.\n")



# analyze each chunk
chunk_summaries = []
for i, chunk in enumerate(chunks):
    print(f"    Analyzing chunk {i+1}/{len(chunks)}...", end="", flush=True)
    chunk_start = time.time()

    chunk_prompt = f"""You are an expert financial analyst. Analyze this section of a video transcript.
List EVERY detail — every stock, asset, company, person, cycle, date, prediction, insight, and opinion mentioned.
Do not summarize. Do not skip anything. Extract every single piece of information.
DO NOT MAKE STUFF UP. Only report what is actually in the text.

Section {i+1} of {len(chunks)}:
{chunk}
"""
    summary = ask_llm(chunk_prompt)
    chunk_summaries.append(summary)
    chunk_elapsed = time.time() - chunk_start
    print(f" done ({chunk_elapsed:.0f}s)")



# save chunk summaries for debugging
chunks_file = audio_file.replace(".mp3", "_chunks.txt")
with open(chunks_file, "w", encoding="utf-8") as f:
    for i, s in enumerate(chunk_summaries):
        f.write(f"\n{'='*50}\n")
        f.write(f"CHUNK {i+1}\n")
        f.write(f"{'='*50}")
        f.write(s)



# final synthesis
print(f"\n Synthesizing final analysis...", end="", flush=True)
all_summaries = "\n\n---\n\n".join(chunk_summaries)

synthesis_prompt = f"""You are an expert financial analyst. Analyze this investing video transcript in thorough detail.

1. SUMMARY (3-5 sentences covering the main thesis)
2. EVERY STOCK, ASSET AND COMPANY MENTIONED (include ticker symbol, and what was said about each one — bullish or bearish, and why)
3. ALL KEY POINTS AND INSIGHTS (do not skip anything interesting or notable. List every distinct point the speaker makes, even minor ones. I want comprehensive coverage, not a high-level summary)
4. ACTIONABLE TAKEAWAYS (what should an investor do based on this information?)
5. ALL TOPICS TOUCHED UPON (list all topics touched upon, their conclusions, and any interesting notes about them)
6. CYCLES: What cycles are mentioned?
7. SENTIMENT (bullish/bearish/neutral for each sector or stock discussed)

Be thorough. Do not omit details. Take your time. I would rather have too much information than too little.

DO NOT MAKE STUFF UP.

Section notes: 
{all_summaries}
"""

full_response = ask_llm(synthesis_prompt)
elapsed = time.time() - start
print(f" done\n Analysis complete. ({elapsed:.0f} seconds total)\n")



# save analysis
analysis_file = audio_file.replace(".mp3", "_analysis.txt")
with open(analysis_file, "w", encoding="utf-8") as f:
    f.write(full_response)

print(f"\n{'='*50}")
print("ANALYIS")
print(f"{'='*50}")
print(full_response)
print(f"\nTranscript saved to: {transcript_file}")
print(f"Chunk details saved to: {chunks_file}")
print(f"Analysis saved to: {analysis_file}")
