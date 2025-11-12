# MCP Toolbox Deployment Scripts

This directory automates the deployment of the GenAI MCP Toolbox to Google Cloud Run, configured for a MySQL database on a Compute Engine VM.

## Deployment Process Overview

The process is a mix of automated scripts and one manual configuration step.

- **Automated Scripts:** Handle infrastructure setup (IAM, Secrets, Networking) and the final build/deploy process.

---

## Deployment Steps

Execute these steps in the following order.

### Step 1: Run GCP Project Initialization
This script enables APIs and creates the service account. It only needs to be run once per project.

```bash
chmod +x 01_setup_gcp_project.sh
./01_setup_gcp_project.sh
```

### Step 2: Run Secrets and Networking Configuration
This script securely stores your database password and creates the VPC Connector.

```bash
chmod +x 02_configure_secrets_and_networking.sh
./02_configure_secrets_and_networking.sh
```

### Step 3: Run the Build and Deploy Script
Now that your configuration is ready, run the final script to build the container and deploy it to Cloud Run.
```bash
chmod +x 03_prepare_and_deploy_mcp.sh
./03_prepare_and_deploy_mcp.sh
```
After this script finishes, it will print the final URL for your MCP Toolbox service.
