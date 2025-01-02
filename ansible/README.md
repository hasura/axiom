# Ansible for Axiom

## Prerequisites

### Install Required Tools
Ensure the necessary tools are installed before proceeding:

```bash
# Install Ansible
brew install ansible

# Install ansible-lint
brew install ansible-lint

# Install Ansible requirements
ansible-galaxy collection install -r requirements.yml
```

## Configure Environment Variables
Set up the `.env` file to include the required database passwords and other sensitive information:

```bash
# Create .env file from the template
cp template.env .env

# Edit the .env file as needed
vim .env
```

## Set Up Inventory of Servers
The Ansible inventory file specifies the servers to manage.

* The official inventory file for presales can be found in the Presales Wiki.
* [Optional] Use the example structure below to create your own inventory file if needed:

```bash
# Create the Ansible inventory file
cat <<EOF > inventory
[demo]
host1 ansible_host=host1.example.com ansible_user=ec2-user ansible_ssh_private_key_file=~/.ssh/id_rsa region=australia ansible_python_interpreter=/usr/bin/python3

[cron]
host1
EOF
```

## Usage
As soon as the server is set up, Ansible can be run against them to complete configuration.

### Run Against All Hosts
Run the playbook against all hosts in your inventory:

```bash
ansible-playbook -i inventory master.yml
```

### Run Against Specific Hosts
To limit execution to specific hosts, use the --limit option:

```bash
ansible-playbook -i inventory master.yml --limit host1:host2:host3
```

### Validate Configuration
Use ansible-lint to validate your playbooks and tasks:

```bash
ansible-lint
```
