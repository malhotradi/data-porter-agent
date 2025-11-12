#!/bin/bash
#
# SCRIPT 2: CONFIGURE SECRETS AND NETWORKING
#
# This script securely stores the MySQL password in Secret Manager and creates
# the Serverless VPC Connector for private network access.
#
echo "--- Step 2: Configuring Secrets and Networking ---"

# Get user input
read -p "Enter your GCP Region (e.g., us-central1): " REGION
read -p "Enter the VPC Network Name your VM is in (usually 'default'): " VPC_NETWORK_NAME
read -s -p "Enter your MySQL root password (will not be displayed): " MYSQL_PASSWORD
echo
echo

# Set variables
export PROJECT_ID=$(gcloud config get-value project)
export SERVICE_ACCOUNT_NAME="mcp-toolbox-sa"
export SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
export MYSQL_SECRET_NAME="mysql-tools"
export VPC_CONNECTOR_NAME="mcp-connector"
export MYSQL_TOOLS_FILE="mysql_tools.yaml"

# --- Secret Management ---
echo "--> Creating secret and storing password..."
# Create the secret
gcloud secrets create ${MYSQL_SECRET_NAME} --replication-policy="automatic"

# Upload your config.yaml file as the secret's value
gcloud secrets versions add ${MYSQL_SECRET_NAME} --data-file=${MYSQL_TOOLS_FILE}

gcloud secrets add-iam-policy-binding ${MYSQL_SECRET_NAME} \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/secretmanager.secretAccessor" --project=${PROJECT_ID}

# --- Networking Setup ---
echo
echo "--> Creating Serverless VPC Connector (this may take a few minutes)..."
gcloud compute networks vpc-access connectors create ${VPC_CONNECTOR_NAME} \
  --region=${REGION} \
  --network=${VPC_NETWORK_NAME} \
  --range=10.8.0.0/28 \
  --project=${PROJECT_ID} || echo "VPC Connector may already exist. Continuing..."

# --- Firewall Rules ---
echo
echo "--> Creating firewall rule to allow traffic on 3306 port of the VM..."
gcloud compute firewall-rules create allow-mysql-from-vpc \
    --allow=tcp:3306 \
    --network=${VPC_NETWORK_NAME} \
    --source-ranges=10.8.0.0/28

echo
echo "✅ Secrets and networking configured. Please run 03_prepare_and_deploy_mcp.sh next."