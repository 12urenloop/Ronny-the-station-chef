## Running the ansible

	ansible-playbook -i hosts.ini playbook.yml

## Running an ad hoc command

	ansible -i hosts.ini station -a 'sudo /sbin/shutdown -t 0'
