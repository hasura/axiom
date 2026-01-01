# Ansible for Axiom

This repository contains Ansible playbooks for deploying and managing Axiom demo environments. The playbooks automate the setup of servers, installation of dependencies, and deployment of Axiom demos.

## Overview

The Ansible setup consists of several playbooks that handle different aspects of the deployment:

- **master.yml**: The main entry point that orchestrates the entire deployment process
- **base.yml**: Base server setup (timezone, hostname, packages, MOTD)
- **manage_ssh_keys.yml**: Manages SSH keys for authorized users
- **configure_docker.yml**: Installs and configures Docker with logging limits
- **axiom.yml**: Syncs demo files and starts containers
- **shelfwise.yml**: ShelfWise-specific setup (Rust toolchain, generator build)
- **nginx.yml**: Nginx reverse proxy setup
- **cron.yml**: Sets up cron jobs for maintenance tasks

## Prerequisites

### Install Required Tools
Ensure the necessary tools are installed before proceeding:

```bash
# Install Ansible
brew install ansible

# Install ansible-lint
brew install ansible-lint

# Install Mitogen for faster execution (from infra/ansible dir)
git clone https://github.com/mitogen-hq/mitogen.git .ansible/mitogen

# Install Ansible requirements (from infra/ansible dir)
ansible-galaxy collection install -r requirements.yml -p .ansible/collections
ansible-galaxy role install -r requirements.yml --roles-path .ansible/roles
```

## Configuration

### Configure Environment Variables
Set up the `.env` file to include the required database passwords and other sensitive information:

```bash
# Create .env file from the template
cp template.env .env

# Edit the .env file as needed
vim .env
```

### Set Up Inventory of Servers
The Ansible inventory file specifies the servers to manage.

* The official inventory file for presales can be found in the Presales Wiki.
* [Optional] Use the example structure below to create your own inventory file if needed:

```bash
# Create the Ansible inventory file
cat <<EOF > inventory.json
{
  "hosts": {
    "vars": {
      "ansible_user": "ubuntu",
      "ansible_ssh_private_key_file": "~/.ssh/id_rsa",
      "ansible_python_interpreter": "/usr/bin/python3"
    },
    "hosts": {
      "telco": {
        "ansible_host": "telco-server.example.com",
        "region": "us-east",
        "demo_profile": "telco"
      }
    }
  }
}
EOF
```

## Usage

### Run Against All Hosts
Run the playbook against all hosts in your inventory:

```bash
ansible-playbook -i inventory.json master.yml
```

### Run Against Specific Hosts
To limit execution to specific hosts, use the --limit option:

```bash
ansible-playbook -i inventory.json master.yml --limit host1:host2:host3
```

### Force Clean Installation
To force a complete reinstallation (stop all containers, remove volumes, and start fresh):

```bash
ansible-playbook -i inventory.json master.yml -e "force_clean=true"
```

### Run Specific Playbooks
You can run specific playbooks individually if needed:

```bash
# Just set up Docker
ansible-playbook -i inventory.json playbooks/configure_docker.yml

# Just set up cron jobs
ansible-playbook -i inventory.json playbooks/cron.yml
```

### Validate Configuration
Use ansible-lint to validate your playbooks and tasks:

```bash
ansible-lint
```

## Playbook Details

### master.yml
The main entry point that imports all other playbooks in the correct order:
- Base server setup
- SSH keys
- Docker
- Axiom demo deployment
- ShelfWise (if applicable)
- Nginx (if applicable)
- Cron jobs

### axiom.yml
The main deployment playbook that:
- Installs prerequisites (DDN CLI)
- Configures Docker
- Clones and configures the Axiom repository
- Sets up environment variables
- Manages Docker containers for the demo
- Provides smart container management (starts if not running, ignores if running)

### cron.yml
Sets up cron jobs for maintenance tasks like connector keepalive.
