.PHONY: test clean

init:
	ansible-galaxy install -r requirements.yml

test:
	vagrant up --provision
	sleep 1 && ./test-station.sh
clean:
	vagrant destroy
