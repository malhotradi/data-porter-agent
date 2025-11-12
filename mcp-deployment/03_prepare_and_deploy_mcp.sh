#!/bin/bash
#
# SCRIPT 3: DEPLOY THE MCP TOOLBOX
#
# This script deploys the official, pre-built MCP Toolbox image to Cloud Run.
#
echo "--- Step 2: Deploying MCP Toolbox to Cloud Run ---"

# --- Get User Input ---
read -p "Enter your GCP Region (e.g., us-central1): " REGION

# --- Set Variables ---
export PROJECT_ID=$(gcloud config get-value project)
export SERVICE_NAME="mcp-toolbox"
export SERVICE_ACCOUNT_EMAIL="mcp-toolbox-sa@${PROJECT_ID}.iam.gserviceaccount.com"
export SECRET_NAME="mysql-tools"
export VPC_CONNECTOR_NAME="mcp-connector"
export MYSQL_TOOLS_FILE="mysql_tools.yaml"
# --- Deploy to Cloud Run ---
echo "--> Deploying the official MCP Toolbox image..."
gcloud run deploy ${SERVICE_NAME} \
  --image="us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest" \
  --service-account=${SERVICE_ACCOUNT_EMAIL} \
  --vpc-connector=${VPC_CONNECTOR_NAME} \
  --set-secrets "/app/${MYSQL_TOOLS_FILE}=${SECRET_NAME}:latest" \
  --args="--tools-file=/app/${MYSQL_TOOLS_FILE}","--address=0.0.0.0","--port=8080" \
  --allow-unauthenticated \
  --region=${REGION} \
  --platform=managed \
  --project=${PROJECT_ID}

# --- Final Output ---
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --platform=managed --region=${REGION} --format='value(status.url)')
echo
echo "✅ ✅ ✅ Deployment Complete! ✅ ✅ ✅"
echo
echo "Your MCP Toolbox URL is: ${SERVICE_URL}"
echo "Use this URL for the 'MCP_SSE_URL' variable in your agent's configuration."
echo "------------------------------------------------------------------"