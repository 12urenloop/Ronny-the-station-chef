# Ronny the station chef

## Setup

```bash
pip3 install -r requirements.txt
```

Install `hclitool` for detecting the bacons.

For now a simple sqlite database is used. This will be updated later on.

## Running

```bash
stdbuf -oL hcitool lescan --duplicates --passive | python3 ronny.py
```

