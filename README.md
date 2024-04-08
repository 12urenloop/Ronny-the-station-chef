# Gonny the station chef

a rewrite of ronny the station chef but in go

## TODO
- [ ] Move all log.fatals to proper err handling
- [ ] Implement Error recovery
- [ ] Add health endpoint

## What is what?

- Collector: Retrieves all packages retrieved on the bluetooth interface, filters out the garbage and stores the baton packets as a detection in the postgresql DB
- Spreader: An HTTP webser powered by [fiber](gofiber.io) with an websocket endpoint where the detections will be sent over.
- Emulator: This will emulate the `Collector` for testing purposes

## Setup

- Install [go](https://go.dev/dl/)

- Run what you want with `go run cmds/PROGRAM/main.go`
and in the case of the `Collector` do not forget to run the program with higher privileges


## Production

There is an all in one Ansible script that sets a linux machine up to run ronny. You need to have **Ansible** and **ansible-galaxy** installed.

Steps:
1. `cd ansible`
2. make init
3. enter the stations in the [hosts.ini](ansible/hosts.ini) file
4. `ansible-playbook playbook.yml`

