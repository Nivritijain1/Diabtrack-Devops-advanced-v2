
# DiabTrack – End-to-End DevOps Implementation

An end-to-end DevOps implementation for a machine-learning-based diabetes risk prediction application using Docker, Terraform, Ansible and Nagios Core.

## Project Overview

DiabTrack is a machine-learning application that predicts diabetes risk using a trained model and scaler.

This project extends the application with containerization, infrastructure provisioning, automated model artifact backups and service monitoring.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and monitoring plugin |
| Streamlit | Application interface |
| Docker | Application containerization |
| Terraform | Docker infrastructure provisioning |
| Ansible | Model artifact backup automation |
| Nagios Core | Application and model monitoring |
| Linux (Ubuntu/WSL2) | Execution environment |

## Architecture

```text
             DiabTrack ML Application
                       |
                  Dockerfile
                       |
                  Docker Image
                       |
                   Terraform
                       |
              Docker Network
                 /        \
                /          \
       Testing Container  Production Container
          Port 8502          Port 8503
                \             /
                 \           /
                  Ansible
                     |
           Model Artifact Backup
                     |
                  Nagios
                     |
          -----------------------
          |                     |
       TCP Checks        Model Readiness
          |                     |
          -----------------------
                     |
               Nagios Dashboard
```

## Implemented Modules

### 1. Docker

- Builds the application image using Python 3.11 Slim.
- Packages application dependencies and trained model artifacts.
- Runs two independent containers:
  - `diabtrack-testing`
  - `diabtrack-production`
- Maps host ports 8502 and 8503 to container port 8501.
- Connects both containers to a shared Docker network.

### 2. Terraform

Terraform provisions the Docker infrastructure through `main.tf`.

Resources:
- Docker image
- Docker network
- Testing container
- Production container

Commands:

```bash
cd terraform
terraform init
terraform validate
terraform plan
terraform apply
```

### 3. Ansible

Ansible automates backups of the two trained model artifacts.

Files backed up:
- `diabetes_model.pkl`
- `diabetes_scaler.pkl`

Backup location:

```text
/var/backups/diabtrack/
```

A cron job is configured to run the backup daily at 2:00 AM.

Run:

```bash
cd ansible
ansible-playbook playbook.yml --ask-become-pass
```

### 4. Nagios Core

Nagios monitors four DiabTrack services:

| Service | Monitoring |
|---|---|
| DiabTrack Testing | TCP port 8502 |
| DiabTrack Production | TCP port 8503 |
| DiabTrack Model Testing | Model readiness test |
| DiabTrack Model Production | Model readiness test |

### 5. Custom Python Monitoring Plugin

The custom plugin `check_model.py`:

1. Receives a container name.
2. Executes a Python command inside that container.
3. Loads the model and scaler.
4. Creates a sample 12-feature input.
5. Applies scaler transformation.
6. Executes `predict()` and `predict_proba()`.
7. Returns Nagios OK or CRITICAL status.

This verifies model execution readiness, not prediction accuracy or clinical validity.

## Project Structure

```text
DiabTrack-DevOps/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── diabetes_model.pkl
│   └── diabetes_scaler.pkl
│
├── terraform/
│   └── main.tf
│
├── ansible/
│   ├── inventory
│   └── playbook.yml
│
├── nagios/
│   └── plugins/
│       └── check_model.py
│
├── .gitignore
└── README.md
```

## Verification

Check Docker containers:

```bash
docker ps
```

Check application endpoints:

```bash
curl -I http://localhost:8502
curl -I http://localhost:8503
```

Check Ansible backups:

```bash
sudo ls -lh /var/backups/diabtrack/
```

Validate Nagios:

```bash
sudo nagios4 -v /etc/nagios4/nagios.cfg
```

## Current Scope and Limitations

- Testing and Production are separate containers using the same image.
- Ansible currently handles only model and scaler backups.
- Nagios performs TCP and model-readiness checks.
- The model plugin performs a smoke test, not accuracy validation.
- The implementation runs on a local Docker environment under Ubuntu/WSL2.
- Automated model retraining, model promotion, CI/CD and Kubernetes are not implemented.

## Future Enhancements

- Automated CI/CD pipeline.
- Model version management.
- Backup restoration and integrity verification.
- Container resource monitoring.
- Cloud deployment.
- Kubernetes orchestration.

## Repository

GitHub: https://github.com/Nivritijain1/Diabtrack-Devops-advanced-v2
