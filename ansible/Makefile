.PHONY: test clean

test:
	vagrant up --provision
	sleep 1 && ./test-station.sh
clean:
	vagrant destroy
