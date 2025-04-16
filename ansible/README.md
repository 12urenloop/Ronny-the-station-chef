## Install roles

```sh
ansible-galaxy role install gantsign.golang
```

```sh
ansible-galaxy collection install prometheus.prometheus
```

## Running the ansible

```sh
ansible-playbook -i hosts.ini playbook.yml
```

## Running an ad hoc command

```sh
ansible -i hosts.ini station -a 'sudo /sbin/shutdown -t 0'
```
