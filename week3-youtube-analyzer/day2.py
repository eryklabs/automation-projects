import sys
import requests
import json



# read the transcript
transcript_file = sys.argv[1]
with open(transcript_file, "r", encoding="utf-8") as f:
    transcript = f.read()

prompt = f"""Analyze this investing video transcript. Provide: 

1. SUMMARY (2-3 sentences)
2. STOCKS / ASSETS MENTIONED (include ticker symbol if possible)
3. KEY TAKEAWAYS for an investor
4. SENTIMENT (bullish/bearish/neutral and why)

Transcript: 
{transcript}
"""



# call ollama API
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "qwen3:14b",
    "prompt": prompt,
    "stream": True,
    "options": {
        "num_predict": 1024
    }
})



# parse response - handle potential multi-line JSON
raw = response.text
print(raw)
print("="*50)
lines = raw.strip().split("\n")
full_response = ""
for line in lines:
    data = json.loads(line)
    if "response" in data:
        full_response += data["response"]

print(full_response)