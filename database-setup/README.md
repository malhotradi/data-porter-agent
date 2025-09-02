### MySQL Database Versions installed
[Docker Image - mysql:5.6](https://hub.docker.com/layers/library/mysql/5.6/images/sha256-897086d07d1efa876224b147397ea8d3147e61dd84dce963aace1d5e9dc2802d) <br>
[Docker Image - mysql:8.0](https://hub.docker.com/layers/library/mysql/8.0/images/sha256-f315ea10389cb76ad6597082b315321dcd2afccc131b35097f8e79e3df5f116b) <br>
[Docker Image - mysql:9.4.0](https://hub.docker.com/layers/library/mysql/9.4.0/images/sha256-e85dc53b71c49afff2047f3ed2dd4ae454da462fcc3e523754e48e36aadd4e2a) <br>

### Compute Engine Setup Command
```
gcloud compute instances create mysql80 \
    --project=data-porter-agent \
    --zone=us-central1-c \
    --machine-type=n1-standard-4 \
    --network-interface=stack-type=IPV4_ONLY,subnet=data-porter-vpc,no-address \
    --metadata=enable-osconfig=TRUE,enable-oslogin=true \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=1041111835370-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=mysql80,disk-resource-policy=projects/data-porter-agent/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/debian-cloud/global/images/debian-12-bookworm-v20250812,mode=rw,size=10,type=pd-balanced \
    --shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ops-agent-policy=v2-x86-template-1-4-0,goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any \
&& \
printf 'agentsRule:\n  packageState: installed\n  version: latest\ninstanceFilter:\n  inclusionLabels:\n  - labels:\n      goog-ops-agent-policy: v2-x86-template-1-4-0\n' > config.yaml \
&& \
gcloud compute instances ops-agents policies create goog-ops-agent-v2-x86-template-1-4-0-us-central1-c \
    --project=data-porter-agent \
    --zone=us-central1-c \
    --file=config.yaml
```

### Bucket Creation for staging the scripts
```
gsutil mb -l us-central1 gs://data-porter-agent-stg-bucket
```

### Docker Setup
Execute the script in the VM (can be setup as startup script on the VM)
```
gsutil cp ~/data-porter-agent/database-setup/docker-setup.sh gs://data-porter-agent-stg-bucket/setup-scripts/
```


### SSH to Compute Engine [mysql56, mysql80, mysql94]

**mysql - 5.6**
```
gcloud compute ssh mysql56 --zone us-central1-c
gsutil cp gs://data-porter-agent-stg-bucket/setup-scripts/docker-setup.sh .
sh docker-setup.sh
sudo docker run -it --name mysql_server -e MYSQL_ROOT_PASSWORD=mysql -p 3306:3306 -d mysql:5.6
sudo docker ps
exit
```

**mysql - 8.0**
```
gcloud compute ssh mysql80 --zone us-central1-c
gsutil cp gs://data-porter-agent-stg-bucket/setup-scripts/docker-setup.sh .
sh docker-setup.sh
sudo docker run -it --name mysql_server -e MYSQL_ROOT_PASSWORD=mysql -p 3306:3306 -d mysql:8.0 --default-authentication-plugin=mysql_native_password
sudo docker ps
exit
```

**mysql - 9.4**
```
gcloud compute ssh mysql94 --zone us-central1-c
gsutil cp gs://data-porter-agent-stg-bucket/setup-scripts/docker-setup.sh .
sh docker-setup.sh
sudo docker run -it --name mysql_server -e MYSQL_ROOT_PASSWORD=mysql -p 3306:3306 -d mysql:9.4
sudo docker ps
exit
```

**Stop Container**
```
sudo docker stop <container name>
sudo docker rm <container name>
```

### Test connection from workstation
**mysql - 5.6**
```
docker run -it --rm mysql mysql -h10.128.0.17 -uroot -p
```

**mysql - 8.0**
```
docker run -it --rm mysql mysql -h10.128.0.18 -uroot -p
```

**mysql - 9.4**
```
docker run -it --rm mysql mysql -h10.128.0.19 -uroot -p
```
