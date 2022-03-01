# Ronny the station chef

## Ronny

The script that collects detections and stores them in a database.

## Station

The api that serves the detections stored in the common database.

## Setup

```bash
pip3 install -r requirements.txt
```

Install `hclitool` for detecting the beacons.

For now a simple sqlite database is used. This will be updated later on.

## Running

### Ronny

```bash
stdbuf -oL hcitool lescan --duplicates --passive | python3 ronny.py
```

### Station

```bash
uvicorn station:app --host 0.0.0.0 --reload
```

For production environments gunicorn is recommended.
