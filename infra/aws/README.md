# Create Axiom Server script

## Prerequisites

### Install Required Tools
Ensure the necessary tools are installed before proceeding:

```bash
# Install AWS command
brew install awscli
```

## Configure Environment Variables
Log in to your AWS account and find the correct environment variables to use with the `aws` command.

> [!NOTE]  
> You will most likely have to use new keys and run these commands often as the session times out quickly.

```bash
export AWS_ACCESS_KEY_ID="foo"
export AWS_SECRET_ACCESS_KEY="foo"
export AWS_SESSION_TOKEN="foobar"
```

## Usage
To set up a new presales demo instance, run this script to provision one automatically. This script will:

* Create a t2.medium host on Ubuntu 22.04 LTS with 25GB storage
* Create a security group which opens appropriate ports:
    * 22 (SSH)
    * 80 (HTTP)
    * 443 (HTTPS)
    * 5432 (Postgres 1)
    * 5433 (Postgres 2)
    * 8787 (Cache)
    * 8123 (Clickhouse)
    * 9000 (Clickhouse)
    * 27017 (MongoDB)
* Create a new PEM for accessing the server
    * Move the PEM to the user's `.ssh` directory
    * Apply appropriate permissions (`chmod 400`)

### Create a new host
Create a new server in ap-northeast-1:

```bash
./create-axiom-server.sh -r ap-northeast-1
```

### Delete the host you just created

```bash
aws ec2 terminate-instances --instance-ids i-d850edd5b99887d1 --region ap-northeast-1
```

### Configuring the server
Once you have the IP address and the generated PEM, you should alter the Ansible `inventory` file by adding a line similar to the below within the `[demo]` group.

```
$host ansible_host=$host-axiom.$domain ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/$pem region=$region ansible_python_interpreter=/usr/bin/python3
```

Change the following:
* $host: Use a descriptive name to refer to the host
* $domain: A domain name that the IP address the script generated points to
* $pem: The location of the PEM file that was created by the script
* $region: The region defined when the server was created