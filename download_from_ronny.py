import requests
from collections import defaultdict
import json
import time
import datetime
import signal


TELRAAM_STATION_URL = 'http://172.12.50.21:8080'

# Max amount of entries to download at once
BLOCKSIZE = 5000

# Maps name to last seen id
last_ids = defaultdict(lambda: 0)

# Maps name to list of detection objects
detectiondata = defaultdict(list)

station_data = requests.get(TELRAAM_STATION_URL + '/station').json()

last_synced_to_files = datetime.datetime.fromtimestamp(0)

allowed_to_save = False

def get_ronny_name(ronny):
    return ''.join(ronny['name'].split(' ')).lower()

def sync_to_files():
    '''Syncs global objects to json files'''
    for ronny in station_data:
        name = get_ronny_name(ronny)
        with open(f'dumps/{name}.json', 'w') as outfile:
            dump = {
                'station_id': name,
                'detections': detectiondata[name]
            }
            json.dump(dump, outfile)

def sync_from_files():
    '''Syncs global objects from json files'''
    global allowed_to_save
    for ronny in station_data:
        name = get_ronny_name(ronny)
        try:
            with open(f'dumps/{name}.json') as infile:
                data = json.load(infile)
                last_ids[name] = max(d['id'] for d in data['detections'])
                detectiondata[name] = data['detections']
            print(f"Loaded {name}")
        except FileNotFoundError:
            print(f"File for {name} not found")
    allowed_to_save = True
    

def signal_handler(_signum, _frame):
    global allowed_to_save
    if allowed_to_save:
        print("Syncing one last time")
        sync_to_files()
    exit(0)


signal.signal(signal.SIGINT, signal_handler)

sync_from_files()
while True:
    for ronny in station_data:
        time.sleep(1)
        name = get_ronny_name(ronny)
        try:
            response = requests.get(f'{ronny["url"]}/detections/{last_ids[name]}?limit={BLOCKSIZE}').json()
            print(f"Request {name} succeeded; was at {last_ids[name]}, got {len(response['detections'])}")    
        except requests.exceptions.RequestException:
            print(f"Failed {name}")
            continue
        if not response['detections']:
            continue
        detectiondata[name].extend(response['detections'])
        last_ids[name] = max(max(detection['id'] for detection in response['detections']), last_ids[name])
    if datetime.datetime.now() - last_synced_to_files > datetime.timedelta(minutes=5):
        sync_to_files()
        print("Syncing to files... ", end='', flush=True)
        last_synced_to_files = datetime.datetime.now()
        print(f"done at {last_synced_to_files.isoformat(' ', 'seconds')}")
