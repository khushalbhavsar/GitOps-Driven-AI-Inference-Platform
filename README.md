# 🚀 GitOps-Driven AI Inference Platform

<p align="center">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white" alt="Jenkins"/>
  <img src="https://img.shields.io/badge/OWASP-000000?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP"/>
  <img src="https://img.shields.io/badge/SonarQube-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white" alt="SonarQube"/>
  <img src="https://img.shields.io/badge/Trivy-1904DA?style=for-the-badge&logo=aquasecurity&logoColor=white" alt="Trivy"/>
  <img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white" alt="ArgoCD"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/AWS_EKS-FF9900?style=for-the-badge&logo=amazoneks&logoColor=white" alt="AWS EKS"/>
  <img src="https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white" alt="Helm"/>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#️-tech-stack)
- [Pipeline Architecture](#-pipeline-architecture)
- [Quick Navigation](#-quick-navigation)
- [Pre-requisites](#-pre-requisites)
- [Installation Guide](#-installation-guide)
- [Application Setup](#-application-setup)
- [Jenkins Configuration](#️-jenkins-configuration)
- [ArgoCD Deployment](#-argocd-deployment)
- [Monitoring Setup](#-monitoring-with-prometheus-and-grafana)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Clean Up](#-clean-up)

---

## 📖 Overview

A production-ready **GitOps-Driven AI Inference Platform** for real-time sentiment analysis. Built with **FastAPI** and **Python 3.11**, deployed to **AWS EKS** using GitOps principles with **Argo CD**, featuring comprehensive CI/CD pipelines with security scanning.

### Key Features

- 🤖 **AI Sentiment Analysis** - Real-time text classification using DistilBERT
- 🔄 **GitOps Workflow** - Automated deployments via Argo CD
- 🔒 **Security Scanning** - OWASP, Trivy, Bandit, Safety
- 📊 **Code Quality** - SonarQube, Flake8, Black, MyPy
- 📈 **Monitoring** - Prometheus metrics & Grafana dashboards
- 🐳 **Multi-stage Docker** - Production-optimized container builds

---

## 🛠️ Tech Stack

| Technology | Purpose |
|:----------:|---------|
| **GitHub** | Source Code Management |
| **Docker** | Containerization (Python 3.11-slim) |
| **Jenkins** | CI Pipeline (Build, Test, Push) |
| **OWASP** | Dependency Vulnerability Check |
| **SonarQube** | Code Quality Analysis |
| **Trivy** | Container & Filesystem Scanning |
| **ArgoCD** | GitOps Continuous Deployment |
| **Redis** | Caching Layer |
| **AWS EKS** | Kubernetes Cluster (v1.30) |
| **Helm** | Prometheus & Grafana Deployment |

---

## 🔄 Pipeline Architecture

### CI Pipeline (Jenkinsfile)

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Checkout │──▶│  Unit    │──▶│  Code    │──▶│ Security │──▶│  Docker  │──▶│  Push    │
│   Code   │   │  Tests   │   │ Quality  │   │   Scan   │   │  Build   │   │  Image   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                    │              │              │
                    ▼              ▼              ▼
               pytest +      Flake8 +       Bandit +
               coverage      Black +        Safety +
                             MyPy          Trivy
```

### CD Pipeline (GitOps Update)

```
┌──────────┐   ┌──────────────────┐   ┌──────────┐
│   CI     │──▶│ Update Image Tag │──▶│   Git    │
│ Success  │   │ in Kustomization │   │   Push   │
└──────────┘   └──────────────────┘   └──────────┘
```

### ArgoCD Sync

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────────────┐
│  GitOps  │──▶│  ArgoCD  │──▶│  Sync    │──▶│  EKS Cluster   │
│   Repo   │   │  Detect  │   │  Apply   │   │  (3 Envs)      │
└──────────┘   └──────────┘   └──────────┘   └────────────────┘
```

---

## 📚 Quick Navigation

| Section | Description |
|---------|-------------|
| [Jenkins Master](#2️⃣-install-jenkins-master-machine) | Install and configure Jenkins |
| [eksctl & EKS](#3️⃣-create-eks-cluster-master-machine) | Create Kubernetes cluster |
| [Jenkins Worker](#4️⃣-setup-jenkins-worker-node) | Configure build agent |
| [SonarQube](#5️⃣-install-sonarqube-master-machine) | Code quality server |
| [Trivy](#6️⃣-install-trivy-jenkins-worker) | Security scanner |
| [ArgoCD](#7️⃣-install-argocd-master-machine) | GitOps deployment |
| [Monitoring](#-monitoring-with-prometheus-and-grafana) | Prometheus & Grafana |
| [Clean Up](#-clean-up) | Delete resources |

---

## 📋 Pre-requisites

> **Note:** This project uses **us-west-1 (N. California)** region.

### AWS Infrastructure

| Machine | Type | vCPU | RAM | Storage | Purpose |
|---------|------|------|-----|---------|---------|
| Master | t2.large | 2 | 8 GB | 29 GB | Jenkins, eksctl, EKS mgmt |
| Worker | t2.large | 2 | 8 GB | 29 GB | Jenkins Agent, Docker builds |

### Security Group Ports

| Port | Service |
|------|---------|
| 22 | SSH |
| 80/443 | HTTP/HTTPS |
| 465 | SMTPS (Email) |
| 6443 | Kubernetes API |
| 8000 | AI Inference App |
| 8080 | Jenkins |
| 9000 | SonarQube |
| 30000-32767 | NodePort |

---

## 🚀 Installation Guide

### 1️⃣ Install Docker (Master Machine)

```bash
sudo apt-get update
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu && newgrp docker
```

---

### 2️⃣ Install Jenkins (Master Machine)

```bash
# Install Java 17
sudo apt update -y
sudo apt install fontconfig openjdk-17-jre -y

# Add Jenkins repo
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update -y
sudo apt-get install jenkins -y
```

**Access:** `http://<master-ip>:8080`

---

### 3️⃣ Create EKS Cluster (Master Machine)

#### Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
aws configure
```

#### Install kubectl

```bash
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
kubectl version --short --client
```

#### Install eksctl

```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

#### Create Cluster

```bash
# Create EKS cluster
eksctl create cluster --name=ai-inference-cluster \
                      --region=us-west-1 \
                      --version=1.30 \
                      --without-nodegroup

# Associate OIDC provider
eksctl utils associate-iam-oidc-provider \
  --region us-west-1 \
  --cluster ai-inference-cluster \
  --approve

# Create node group
eksctl create nodegroup --cluster=ai-inference-cluster \
                        --region=us-west-1 \
                        --name=ai-inference-nodes \
                        --node-type=t2.large \
                        --nodes=2 \
                        --nodes-min=2 \
                        --nodes-max=2 \
                        --node-volume-size=29 \
                        --ssh-access \
                        --ssh-public-key=eks-nodegroup-key
```

---

### 4️⃣ Setup Jenkins Worker Node

#### Install Java

```bash
sudo apt update -y
sudo apt install fontconfig openjdk-17-jre -y
```

#### Attach IAM Role
- EC2 → Actions → Security → Modify IAM role → **Administrator Access**

#### Configure AWS CLI

```bash
sudo su
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
aws configure
```

#### Add Node in Jenkins

**Manage Jenkins** → **Nodes** → **New Node**

| Setting | Value |
|---------|-------|
| Name | `Node` |
| Remote Root | `/home/ubuntu` |
| Labels | `Node` |
| Launch | Via SSH |
| Host | `<worker-ip>` |

#### Install Docker on Worker

```bash
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu && newgrp docker
chmod 777 /var/run/docker.sock
```

---

### 5️⃣ Install SonarQube (Master Machine)

```bash
docker run -itd --name SonarQube-Server -p 9000:9000 sonarqube:lts-community
```

**Access:** `http://<master-ip>:9000` (admin/admin)

---

### 6️⃣ Install Trivy (Jenkins Worker)

```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update -y
sudo apt-get install trivy -y
```

---

### 7️⃣ Install ArgoCD (Master Machine)

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods
watch kubectl get pods -n argocd

# Install CLI
sudo curl --silent --location -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.4.7/argocd-linux-amd64
sudo chmod +x /usr/local/bin/argocd

# Expose ArgoCD
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'

# Get password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

---

## 🐍 Application Setup

### Local Development

```bash
cd gitops-ai-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
cd gitops-ai-app

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ \
    --cov=src \
    --cov-report=xml \
    --cov-report=html \
    -v
```

### Code Quality Checks

```bash
# Linting
pip install flake8 black mypy
flake8 src/ --max-line-length=100 --ignore=E501,W503
black --check src/ --line-length=100
mypy src/ --ignore-missing-imports

# Security scan
pip install bandit safety
bandit -r src/ -f json -o bandit-report.json
safety check -r requirements.txt
```

### Docker Build

```bash
cd gitops-ai-app

# Build production image
docker build --target production -t ai-inference:latest .

# Build development image
docker build --target development -t ai-inference:dev .

# Run container
docker run -p 8000:8000 \
    -e LOG_LEVEL=INFO \
    -e WORKERS=4 \
    --name ai-inference \
    ai-inference:latest

# Test health endpoint
curl http://localhost:8000/health
```

---

## ⚙️ Jenkins Configuration

### Required Plugins

- ✅ OWASP Dependency-Check
- ✅ SonarQube Scanner
- ✅ Docker Pipeline
- ✅ Pipeline: Stage View
- ✅ Git

### Add Credentials

| ID | Type | Description |
|----|------|-------------|
| `docker-registry-url` | Secret text | Docker registry URL |
| `docker-registry-credentials` | Username/Password | Docker Hub login |
| `gitops-repo-credentials` | Username/Password | GitHub PAT |
| `sonarqube-token` | Secret text | SonarQube token |

### Configure Tools

**Manage Jenkins** → **Tools**:

| Tool | Name | Install |
|------|------|---------|
| Dependency-Check | `DP-Check` | Auto |
| SonarQube Scanner | `SonarScanner` | Auto |

### SonarQube Webhook

**SonarQube** → **Administration** → **Webhooks** → **Create**
- URL: `http://<jenkins-ip>:8080/sonarqube-webhook/`

### Create Pipeline Jobs

#### CI Pipeline (ai-inference-ci)

| Setting | Value |
|---------|-------|
| Pipeline | Pipeline script from SCM |
| SCM | Git |
| Repository | `https://github.com/your-org/gitops-ai-app.git` |
| Script Path | `Jenkinsfile` |

---

## 🎯 ArgoCD Deployment

### Connect Cluster

```bash
# Login
argocd login <argocd-url>:<port> --username admin

# Add cluster
kubectl config get-contexts
argocd cluster add <context-name> --name ai-inference-cluster
```

### Deploy Applications

```bash
# Apply ArgoCD projects
kubectl apply -f gitops-manifests/argocd/projects.yaml

# Apply root application (App of Apps)
kubectl apply -f gitops-manifests/argocd/root-app.yaml
```

### ArgoCD Applications Created

| Application | Namespace | Path | Sync |
|-------------|-----------|------|------|
| `ai-inference-dev` | ai-inference-dev | `apps/ai-inference/overlays/dev` | Auto |
| `ai-inference-staging` | ai-inference-staging | `apps/ai-inference/overlays/staging` | Auto |
| `ai-inference-prod` | ai-inference-prod | `apps/ai-inference/overlays/prod` | Manual |
| `monitoring` | monitoring | `monitoring` | Auto |

### Verify Deployment

```bash
# Check ArgoCD apps
argocd app list

# Check pods
kubectl get pods -n ai-inference-dev
kubectl get pods -n ai-inference-staging
kubectl get pods -n ai-inference-prod

# Check services
kubectl get svc -n ai-inference-dev
```

---

## 📊 Monitoring with Prometheus and Grafana

### Install Helm

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### Deploy Prometheus Stack

```bash
# Add repos
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Install
kubectl create namespace prometheus
helm install stable prometheus-community/kube-prometheus-stack -n prometheus

# Expose services
kubectl patch svc stable-kube-prometheus-sta-prometheus -n prometheus -p '{"spec": {"type": "NodePort"}}'
kubectl patch svc stable-grafana -n prometheus -p '{"spec": {"type": "NodePort"}}'

# Get Grafana password
kubectl get secret --namespace prometheus stable-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

### Application Metrics

The AI Inference app exposes these Prometheus metrics at `/metrics`:

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | Request latency |
| `predictions_total` | Counter | Total predictions |
| `prediction_duration_seconds` | Histogram | Inference time |

---

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe |
| GET | `/metrics` | Prometheus metrics |
| POST | `/api/v1/predict` | Single prediction |
| POST | `/api/v1/predict/batch` | Batch predictions |

### Example: Single Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

**Response:**
```json
{
  "success": true,
  "result": {
    "text": "This product is amazing!",
    "label": "POSITIVE",
    "confidence": 0.95,
    "sentiment_score": 0.89,
    "processing_time_ms": 23.5
  },
  "model": "distilbert-base-uncased-finetuned-sst-2-english",
  "timestamp": "2026-01-01T10:30:00Z",
  "request_id": "abc123"
}
```

### Example: Batch Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great!", "Terrible!", "Okay"]}'
```

---

## 📁 Project Structure

```
GitOps-Driven-AI-Inference-Platform/
│
├── gitops-ai-app/                      # Application Repository
│   ├── src/
│   │   ├── main.py                     # FastAPI app (uvicorn)
│   │   ├── config.py                   # Environment config
│   │   ├── api/
│   │   │   └── predict.py              # /api/v1/predict endpoint
│   │   ├── models/
│   │   │   └── sentiment_model.py      # DistilBERT model
│   │   ├── services/
│   │   │   └── inference_service.py    # ML inference logic
│   │   └── utils/
│   │       └── preprocessing.py        # Text preprocessing
│   ├── tests/
│   │   ├── test_api.py                 # API tests
│   │   └── test_inference.py           # Inference tests
│   ├── Dockerfile                      # Multi-stage (builder/production/dev)
│   ├── Jenkinsfile                     # CI pipeline
│   ├── Jenkinsfile.pr                  # PR validation
│   ├── requirements.txt                # Python deps
│   ├── pyproject.toml                  # Project config
│   └── pytest.ini                      # Test config
│
├── gitops-manifests/                   # GitOps Repository
│   ├── argocd/
│   │   ├── root-app.yaml               # App of Apps bootstrap
│   │   └── projects.yaml               # RBAC & projects
│   ├── apps/
│   │   └── ai-inference/
│   │       ├── base/
│   │       │   ├── deployment.yaml     # 2 replicas, resources, probes
│   │       │   ├── service.yaml        # ClusterIP port 80→8000
│   │       │   ├── hpa.yaml            # Autoscaling
│   │       │   └── kustomization.yaml  # Base config
│   │       └── overlays/
│   │           ├── dev/                # 1 replica
│   │           ├── staging/            # 2 replicas
│   │           └── prod/               # 3 replicas, ingress
│   └── monitoring/
│       ├── prometheus/
│       │   └── values.yaml
│       └── grafana/
│           └── dashboards/
│               └── ai-inference-dashboard.json
│
└── README.md
```

---

## 🌍 Environments

| Environment | Namespace | Replicas | Resources | Sync |
|-------------|-----------|----------|-----------|------|
| **Dev** | ai-inference-dev | 1 | 256m/512Mi | Auto |
| **Staging** | ai-inference-staging | 2 | 500m/1Gi | Auto |
| **Production** | ai-inference-prod | 3 | 1000m/2Gi | Manual |

---

## 🧹 Clean Up

### Delete EKS Cluster

```bash
eksctl delete cluster --name=ai-inference-cluster --region=us-west-1
```

### Delete ArgoCD Apps

```bash
argocd app delete ai-inference-dev
argocd app delete ai-inference-staging
argocd app delete ai-inference-prod
argocd app delete monitoring
```

### Terminate EC2 Instances

AWS Console → EC2 → Select instances → **Terminate**

### Clean Docker

```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker system prune -a
```

---

## 📧 Email Notification Setup

### Gmail App Password

1. Enable **2-Step Verification**
2. Gmail → **Manage Account** → **Security** → **App passwords**
3. Create password for Jenkins

### Jenkins Configuration

**Manage Jenkins** → **System** → **Extended E-mail Notification**

| Setting | Value |
|---------|-------|
| SMTP Server | smtp.gmail.com |
| SMTP Port | 465 |
| Use SSL | ✅ |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>🚀 GitOps-Driven AI Inference Platform</b><br>
  Built with FastAPI • Deployed with ArgoCD • Secured with DevSecOps
</p>
