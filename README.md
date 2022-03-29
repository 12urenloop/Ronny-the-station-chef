# Ronny the station chef

## Ronny

The script that collects detections and stores them in a database.

## Station

The api that serves the detections stored in the common database.

## Development

### Setup

```bash
pip3 install -r requirements.txt
```

For now a simple sqlite database is used. This will be updated later on.

### Running

#### Ronny

```bash
python3 ronny.py
```

#### Station

```bash
uvicorn station:app --host 0.0.0.0 --reload
```

For production environments gunicorn is recommended.

## Production

There is an all in one Ansible script that sets a linux machine up to run ronny. You need to have **Ansible** and **ansible-galaxy** installed.

Steps:
1. `cd ansible`
2. make init
3. enter the stations in the [hosts.ini](ansible/hosts.ini) file
4. `ansible-playbook playbook.yml`

### Testing

To test a production deployment, go into the Ansible folder and run `make test`.

This will create a Vagrant VM and will run the Ansible script locally onto that VM.
