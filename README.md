# Data Migration Assistant

### Python Setup steps
```
cd ~
sudo apt-get update
sudo apt-get install python3.12-venv
python -m venv venv
source ~/venv/bin/activate
```

### Github Clone
```
git clone https://github.com/murlik1/logsense.git
```

### Python Library Setup
```
cd ~/data-porter-agent
source ~/venv/bin/activate
python -m pip install -r requirements.txt
```

### Setup Authentication
```
gcloud auth revoke
gcloud auth application-default revoke
unset GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
gcloud config set billing/quota_project data-porter-agent
gcloud config set project data-porter-agent
```

