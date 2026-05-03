transcript-screener/
├── README.md                          # What this is, current status, last updated date
├── prompts/
│   ├── stage1_extraction_v2.md        # The full Stage 1 prompt
│   ├── stage2a_canslim_v1.md          # Stage 2A 
│   ├── stage2b_superstocks_v3.md      # Stage 2B
│   └── CHANGELOG.md                   # Version history with rationale
├── docs/
│   ├── methodology_research.md        # The original deep-research artifact
│   ├── stine_book_notes.md            # Your Stine-specific findings
│   ├── canslim_reference.md           # O'Neil bars summarized
│   ├── workflow.md                    # How to actually run this
│   └── decisions_log.md               # Why you made each design call
├── transcripts/
│   ├── _raw/                          # Pasted from Seeking Alpha etc., one folder per ticker
│   │   └── NVDA/
│   │       ├── FY24Q1_2023-05-24.txt
│   │       └── FY24Q2_2023-08-23.txt
│   └── _processed/                    # Concatenated, ready to feed into Stage 1
│       └── NVDA/
│           └── 4Q_concatenated_2023-08-23.txt
├── outputs/
│   └── NVDA/
│       └── 2023-08-23/
│           ├── stage1_extraction.md
│           ├── stage2a_canslim.md
│           ├── stage2b_superstocks.md
│           └── notes.md               # Your own takeaways
├── backtest/
│   ├── known_winners.md               # NVDA, SMCI, ELF, CELH targets + dates
│   ├── known_failures.md              # PTON, DOCU targets + dates  
│   └── results/                       # Stage outputs vs. expected verdicts
├── preprocessor/                      # Empty for now; future Python work
└── .gitignore                         # Exclude /transcripts/_raw if you have copyright concerns



