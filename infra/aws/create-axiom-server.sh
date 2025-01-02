#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display usage
usage() {
  echo "Usage: $0 -r <region>"
  echo ""
  echo "Arguments:"
  echo "  -r <region>  AWS region (e.g., us-east-1)"
  exit 1
}

# Parse arguments
while getopts "r:" opt; do
  case $opt in
    r) REGION="$OPTARG" ;;
    *) usage ;;
  esac
done

# Ensure the region is provided
if [[ -z "$REGION" ]]; then
  echo "Error: Missing required argument: -r <region>"
  usage
fi

# Fixed parameters
INSTANCE_TYPE="t2.medium"
VOLUME_SIZE=25
SG_NAME="presales-sg"
SG_DESCRIPTION="presales sg with required ports"
PORTS=(22 80 443 5432 5433 8123 8787 9000 27017)

# Generate the key name based on region and date
DATETIME=$(date +%Y%m%d-%H%M%S)
KEY_NAME="presales-demo-${REGION}-${DATETIME}"

SSH_DIR="$HOME/.ssh"
KEY_PATH="$SSH_DIR/${KEY_NAME}.pem"

# Fetch the AMI ID for Ubuntu 22.04 LTS in the specified region
echo "Fetching the latest Ubuntu 22.04 LTS AMI ID for region: $REGION..."
AMI_ID=$(aws ec2 describe-images \
  --region "$REGION" \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
            "Name=state,Values=available" \
  --query "Images | sort_by(@, &CreationDate) | [-1].ImageId" \
  --output text)

if [[ "$AMI_ID" == "None" ]]; then
  echo "Error: Unable to fetch the AMI ID for Ubuntu 22.04 LTS in region $REGION."
  exit 1
fi

echo "Using AMI ID: $AMI_ID"

# Create the EC2 key pair
echo "Creating an EC2 key pair: $KEY_NAME..."
aws ec2 create-key-pair \
  --region "$REGION" \
  --key-name "$KEY_NAME" \
  --query "KeyMaterial" \
  --output text > "$KEY_PATH"
chmod 400 "$KEY_PATH"

# Create the security group
echo "Creating security group: $SG_NAME..."
SG_ID=$(aws ec2 create-security-group \
  --group-name "$SG_NAME" \
  --description "$SG_DESCRIPTION" \
  --region "$REGION" \
  --query "GroupId" \
  --output text)

# Add rules to the security group
echo "Adding rules to security group..."
for PORT in "${PORTS[@]}"; do
  OK=$(aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp \
    --port "$PORT" \
    --cidr 0.0.0.0/0 \
    --region "$REGION")
  echo "Port $PORT added to security group."
done

# Launch the EC2 instance
echo "Creating EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --count 1 \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --security-group-ids "$SG_ID" \
  --region "$REGION" \
  --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$VOLUME_SIZE,\"DeleteOnTermination\":true}}]" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=PRESALES-AXIOM}]" \
  --query "Instances[0].InstanceId" \
  --output text)

echo "Instance created with ID: $INSTANCE_ID"

# Wait for the instance to be running
echo "Waiting for the instance to initialize..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID" --region "$REGION"

# # Get the public IP of the instance
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION" \
  --query "Reservations[0].Instances[0].PublicIpAddress" \
  --output text)

echo "Instance is now running"
echo "Public IP: $PUBLIC_IP"
echo "Region: $REGION"
echo "Instance ID: $INSTANCE_ID"
echo "Delete command: aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region $REGION" 
# Output SSH command
# echo "Connect to your instance using the following command:"
# echo "ssh -i ${KEY_PATH} ubuntu@$PUBLIC_IP"
