# voice-notes-to-tasks

A local Python tool for transcribing voice notes to text using Whisper, with planned features for extracting structured information (action items, ideas, project mentions) from the transcripts.

**Status:** Week 6 project — early MVP. Currently transcription only.

## What it does today

Takes an audio file (.m4a, .mp3, .wav, .mp4) and outputs a timestamped text transcript using OpenAI's Whisper (via the faster-whisper library). Supports GPU acceleration on NVIDIA hardware.

```
voice_note.m4a  →  voice_note_transcript.txt
```

## What it will do later

- Run a local LLM over the transcript to extract:
  - Action items
  - Ideas mentioned
  - Projects referenced
  - Summary
- Save structured output as Markdown for Obsidian
- Watch an input folder and process files automatically
- Index transcripts in SQLite for search

None of that is built yet. This README will be updated as features ship.

## Why this exists

I record voice notes while driving. They sit on my phone unused because re-listening to a 20-minute ramble to find the one useful idea takes more time than the idea was worth. This tool turns voice into text I can skim, search, and feed into other tools.

It's also a learning project — local Whisper, Python venvs, GPU acceleration via CUDA, eventually local LLM integration via Ollama.

## Requirements

- Python 3.10+
- ffmpeg (required by Whisper to decode audio)
- ~3GB disk space for the large-v3 Whisper model (downloaded automatically on first run)
- For GPU acceleration: NVIDIA GPU with CUDA support

Tested on:
- Windows 11, Python 3.12, NVIDIA RTX 5060 Ti 16GB — GPU mode confirmed working

## Setup

Clone the repo and create a virtual environment:

```powershell
git clone <repo-url>
cd week6-voice-notes-to-tasks
python -m venv .venv
.venv\Scripts\activate    # Windows PowerShell
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

Install ffmpeg if you don't have it:

```powershell
winget install ffmpeg     # Windows
# brew install ffmpeg       # Mac
# sudo apt install ffmpeg   # Debian/Ubuntu
```

Verify ffmpeg is on PATH (you may need to restart the shell after installing):

```bash
ffmpeg -version
```

## Usage

Defaults: large-v3 model, GPU (CUDA).

```bash
python transcribe.py path/to/audio_file.m4a
```

Override model size or device:

```bash
python transcribe.py audio.m4a small cpu
python transcribe.py audio.m4a medium cuda
```

Output is saved next to the input file as `<filename>_transcript.txt`.

The script prints a startup banner showing what model and device it's using, plus timing info at the end:

```
============================================================
Audio file:    voice_note.m4a
Model:         large-v3
Device:        cuda
Compute type:  float16
Output:        voice_note_transcript.txt
============================================================

Loading model...
Model loaded in 24.3s

Transcribing...
Detected language: en (confidence: 0.99)
Audio duration:    1245.3s (20.8 min)

[0.0s -> 4.2s] So I was thinking about this stock screener idea
[4.2s -> 9.1s] and it would be cool if it could pull data from FMP
...

============================================================
Transcription complete
Time elapsed:     142.6s
Realtime factor:  8.7x
Transcript saved: voice_note_transcript.txt
============================================================
```

The realtime factor tells you how many seconds of audio got processed per second of wall-clock time. GPU mode on large-v3 typically runs 5-15x realtime; CPU mode is usually under 1x.

## Verifying GPU is actually being used

If you pass `cuda` but suspect it's silently falling back to CPU, run this in a separate PowerShell window while transcription is in progress:

```powershell
nvidia-smi -l 2
```

Look at the Processes section at the bottom — your `python.exe` should appear with GPU memory in the GB range. GPU-Util should hover between 20-80% during transcription.

If you see no python process listed, CUDA isn't being used. Most common fix on Windows:

```powershell
pip install nvidia-cudnn-cu12 nvidia-cublas-cu12
```

## Model selection

| Model | Size | Speed (CPU) | Speed (GPU) | Quality |
|-------|------|-------------|-------------|---------|
| tiny | ~75MB | Very fast | Instant | Poor |
| base | ~150MB | Fast | Instant | OK |
| small | ~500MB | Moderate | Very fast | Good |
| medium | ~1.5GB | Slow | Fast | Very good |
| large-v3 | ~3GB | Very slow | Moderate | Best |

The first run with a given model downloads it once. Subsequent runs reuse the cached model from `~/.cache/huggingface/`.

GPU acceleration is dramatically faster — typically 10-20x over CPU for the same model. Quality is identical between GPU and CPU; only the speed differs.

## Project structure

```
week6-voice-notes-to-tasks/
├── README.md
├── requirements.txt
├── transcribe.py        # Single-file MVP
└── .venv/               # Local virtual environment (gitignored)
```

This will grow as features are added. Planned next:

```
├── modules/
│   ├── transcribe.py
│   ├── summarize.py     # Local LLM extraction
│   └── obsidian.py      # Markdown export
├── input/               # Drop new audio here
├── processed/           # Audio files moved here after processing
└── output/              # Transcripts and structured analysis
```

## Roadmap

- [x] Transcribe a single audio file from CLI
- [x] GPU acceleration via CUDA
- [x] Configurable model size and device via CLI args
- [x] Verbose logging with timing and realtime factor
- [ ] Local LLM analysis of transcripts (Ollama or Claude API)
- [ ] Structured Markdown output (summary, action items, ideas, projects)
- [ ] Obsidian export
- [ ] Folder watcher to auto-process new files
- [ ] SQLite index of all processed notes
- [ ] Streamlit UI to browse and search transcripts

## Known issues / honest notes

- First run downloads the Whisper model with no progress bar — large-v3 is ~3GB, allow several minutes before assuming it's hung.
- If GPU mode fails with a CUDA error, install the CUDA runtime libraries (already in `requirements.txt`): `pip install nvidia-cudnn-cu12 nvidia-cublas-cu12`.
- No error handling for unsupported file formats — it'll fail with whatever ffmpeg says.
- No batch mode. One file at a time.
- Output filenames just append `_transcript` to the input — no timestamped runs, so re-running overwrites.

## License

Personal project. No license assigned yet.