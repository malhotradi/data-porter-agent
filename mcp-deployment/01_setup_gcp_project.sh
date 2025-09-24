#!/bin/bash
#
# SCRIPT 1: GCP PROJECT INITIALIZATION
#
# This script enables the necessary APIs and creates a dedicated 
# service account for the MCP Toolbox.
#
echo "--- Step 1: Initializing GCP Project ---"

# Set project-level variables
export PROJECT_ID=$(gcloud config get-value project)
export SERVICE_ACCOUNT_NAME="mcp-toolbox-sa"
export SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# --- Enable Google Cloud APIs ---
echo
echo "--> Enabling necessary Google Cloud APIs..."
gcloud services enable \
  run.googleapis.com \
  secretmanager.googleapis.com \
  vpcaccess.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  --project=${PROJECT_ID}

# --- Create the Service Account ---
echo
echo "--> Creating Service Account: ${SERVICE_ACCOUNT_NAME}..."
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
  --display-name="MCP Toolbox Service Account" \
  --project=${PROJECT_ID} || echo "Service account may already exist. Continuing..."

echo
echo "✅ Project setup complete. Please run 02_configure_secrets_and_networking.sh next."