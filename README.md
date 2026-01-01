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
  - [Docker Installation](#1️⃣-install-docker-master-machine)
  - [Jenkins Master Setup](#2️⃣-install-and-configure-jenkins-master-machine)
  - [EKS Cluster Setup](#3️⃣-create-eks-cluster-on-aws-master-machine)
  - [Jenkins Worker Setup](#4️⃣-setting-up-jenkins-worker-node)
  - [SonarQube Setup](#5️⃣-install-and-configure-sonarqube-master-machine)
  - [Trivy Setup](#6️⃣-install-trivy-jenkins-worker)
  - [ArgoCD Setup](#7️⃣-install-and-configure-argocd-master-machine)
- [Jenkins Configuration](#️-jenkins-configuration)
- [Email Notification Setup](#-email-notification-setup)
- [Monitoring Setup](#-monitoring-with-prometheus-and-grafana)
- [Project Structure](#-project-structure)
- [Clean Up](#-clean-up)

---

## 📖 Overview

A production-ready **GitOps-Driven AI Inference Platform** demonstrating modern cloud-native DevSecOps practices. This platform provides real-time sentiment analysis using a FastAPI-based microservice, deployed to **AWS EKS** via GitOps principles using **Argo CD**, with comprehensive CI/CD pipelines, security scanning, and monitoring.

---

## 🛠️ Tech Stack

| Technology | Purpose | Description |
|:----------:|---------|-------------|
| **GitHub** | Code | Source code management and version control |
| **Docker** | Containerization | Container runtime and image building |
| **Jenkins** | CI | Continuous Integration pipeline automation |
| **OWASP** | Security | Dependency vulnerability checking |
| **SonarQube** | Quality | Static code analysis and quality gates |
| **Trivy** | Security | Container and filesystem vulnerability scanning |
| **ArgoCD** | CD | GitOps-based continuous deployment |
| **Redis** | Caching | In-memory data caching layer |
| **AWS EKS** | Kubernetes | Managed Kubernetes cluster on AWS |
| **Helm** | Monitoring | Package manager for Prometheus & Grafana |

---

## 🔄 Pipeline Architecture

### CI Pipeline - Build and Push Image

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Checkout  │──▶│ SonarQube  │──▶│   OWASP    │──▶│   Trivy    │──▶│   Docker   │
│    Code    │   │  Analysis  │   │ Dep Check  │   │  FS Scan   │   │ Build/Push │
└────────────┘   └────────────┘   └────────────┘   └────────────┘   └────────────┘
```

### CD Pipeline - Update Application Version

```
┌────────────┐   ┌────────────┐   ┌────────────┐
│  Trigger   │──▶│   Update   │──▶│ Git Commit │
│  from CI   │   │ Image Tag  │   │   & Push   │
└────────────┘   └────────────┘   └────────────┘
```

### ArgoCD - Deployment on EKS

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Git Repo  │──▶│   ArgoCD   │──▶│  Sync to   │──▶│  AWS EKS   │
│   Change   │   │   Detect   │   │  Cluster   │   │ Deployment │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
```

---

## 📚 Quick Navigation

> **Important:** Below table helps you navigate to the particular tool installation section fast.

| Tech Stack | Installation Section |
|------------|---------------------|
| Jenkins Master | [Install Jenkins](#2️⃣-install-and-configure-jenkins-master-machine) |
| eksctl | [Install eksctl](#install-eksctl) |
| ArgoCD | [Install ArgoCD](#7️⃣-install-and-configure-argocd-master-machine) |
| Jenkins Worker | [Setup Worker Node](#4️⃣-setting-up-jenkins-worker-node) |
| OWASP | [Configure OWASP](#configure-owasp) |
| SonarQube | [Install SonarQube](#5️⃣-install-and-configure-sonarqube-master-machine) |
| Email Setup | [Email Notifications](#-email-notification-setup) |
| Monitoring | [Prometheus & Grafana](#-monitoring-with-prometheus-and-grafana) |
| Clean Up | [Clean Up Resources](#-clean-up) |

---

## 📋 Pre-requisites

> **Note:** This project will be implemented on **N. California region (us-west-1)**.

### Infrastructure Requirements

| Machine | Instance Type | vCPU | RAM | Storage | Purpose |
|---------|--------------|------|-----|---------|---------|
| Master | t2.large | 2 | 8 GB | 29 GB | Jenkins Master, eksctl, EKS management |
| Worker | t2.large | 2 | 8 GB | 29 GB | Jenkins Worker, Build agents |

### Required Security Group Ports

| Port | Protocol | Service |
|------|----------|---------|
| 22 | TCP | SSH |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 465 | TCP | SMTPS (Email) |
| 6443 | TCP | Kubernetes API |
| 8080 | TCP | Jenkins |
| 9000 | TCP | SonarQube |
| 30000-32767 | TCP | NodePort Services |

---

## 🚀 Installation Guide

### 1️⃣ Install Docker (Master Machine)

```bash
sudo apt-get update
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu && newgrp docker
```

> **Note:** `newgrp docker` refreshes the group config - no restart needed.

---

### 2️⃣ Install and Configure Jenkins (Master Machine)

```bash
# Update and install Java
sudo apt update -y
sudo apt install fontconfig openjdk-17-jre -y

# Add Jenkins repository
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update -y
sudo apt-get install jenkins -y
```

**Access Jenkins:** `http://<master-public-ip>:8080`

---

### 3️⃣ Create EKS Cluster on AWS (Master Machine)

#### Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
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

#### Create EKS Cluster

```bash
eksctl create cluster --name=wanderlust \
                      --region=us-west-1 \
                      --version=1.30 \
                      --without-nodegroup
```

#### Associate IAM OIDC Provider

```bash
eksctl utils associate-iam-oidc-provider \
  --region us-west-1 \
  --cluster wanderlust \
  --approve
```

#### Create Node Group

```bash
eksctl create nodegroup --cluster=wanderlust \
                        --region=us-west-1 \
                        --name=wanderlust \
                        --node-type=t2.large \
                        --nodes=2 \
                        --nodes-min=2 \
                        --nodes-max=2 \
                        --node-volume-size=29 \
                        --ssh-access \
                        --ssh-public-key=eks-nodegroup-key
```

> **Note:** Ensure `eks-nodegroup-key` exists in your AWS account.

---

### 4️⃣ Setting up Jenkins Worker Node

#### Create EC2 Instance
- **Instance Type:** t2.large (2 vCPU, 8GB RAM)
- **Storage:** 29 GB

#### Install Java

```bash
sudo apt update -y
sudo apt install fontconfig openjdk-17-jre -y
```

#### Attach IAM Role
1. Select Jenkins Worker EC2 → **Actions** → **Security** → **Modify IAM role**
2. Attach role with **Administrator Access**

#### Configure AWS CLI

```bash
sudo su
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
aws configure
```

#### Generate SSH Keys (On Master)

```bash
ssh-keygen
# Copy ~/.ssh/id_rsa.pub content to Worker's ~/.ssh/authorized_keys
```

#### Add Node in Jenkins

Navigate to **Manage Jenkins** → **Nodes** → **Add Node**

| Setting | Value |
|---------|-------|
| Name | Node |
| Type | Permanent Agent |
| Executors | 2 |
| Remote Root Directory | /home/ubuntu |
| Labels | Node |
| Launch Method | Via SSH |
| Host | `<worker-public-ip>` |
| Credentials | SSH with private key |
| Host Key Verification | Non verifying |

#### Install Docker on Worker

```bash
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu && newgrp docker
```

---

### 5️⃣ Install and Configure SonarQube (Master Machine)

```bash
docker run -itd --name SonarQube-Server -p 9000:9000 sonarqube:lts-community
```

**Access:** `http://<master-ip>:9000`  
**Default Credentials:** admin / admin

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

### 7️⃣ Install and Configure ArgoCD (Master Machine)

#### Create Namespace and Install

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
watch kubectl get pods -n argocd
```

#### Install ArgoCD CLI

```bash
sudo curl --silent --location -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.4.7/argocd-linux-amd64
sudo chmod +x /usr/local/bin/argocd
```

#### Expose ArgoCD Server

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
kubectl get svc -n argocd
```

#### Get Initial Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

**Access:** `https://<worker-public-ip>:<nodeport>`  
**Username:** admin

---

## ⚙️ Jenkins Configuration

### Required Plugins

Install via **Manage Jenkins** → **Plugins** → **Available**:

- ✅ OWASP Dependency-Check
- ✅ SonarQube Scanner
- ✅ Docker Pipeline
- ✅ Pipeline: Stage View

### Configure OWASP

**Manage Jenkins** → **Tools** → **Dependency-Check installations**
- Name: `DP-Check`
- Install automatically: ✅

### Configure SonarQube

1. **Create Token in SonarQube:**
   - Administration → Security → Users → Token

2. **Add Credentials in Jenkins:**
   - Manage Jenkins → Credentials → Add Secret text

3. **Configure Scanner:**
   - Manage Jenkins → Tools → SonarQube Scanner

4. **Add SonarQube Server:**
   - Manage Jenkins → System → SonarQube installations

5. **Create Webhook in SonarQube:**
   - Administration → Webhooks → Create
   - URL: `http://<jenkins-ip>:8080/sonarqube-webhook/`

### Add Credentials

| Credential | Type | ID |
|------------|------|-----|
| GitHub | Username/PAT | github-credentials |
| Docker Hub | Username/Password | docker-credentials |
| SonarQube | Secret text | sonarqube-token |

### Fix Docker Socket Permission

```bash
chmod 777 /var/run/docker.sock
```

---

## 📧 Email Notification Setup

### Gmail App Password

> **Important:** Enable 2-Step Verification first!

1. Gmail → **Manage Google Account** → **Security**
2. Search **App passwords** → Create for Jenkins

### Configure in Jenkins

**Manage Jenkins** → **System** → **Extended E-mail Notification**

| Setting | Value |
|---------|-------|
| SMTP Server | smtp.gmail.com |
| SMTP Port | 465 |
| Use SSL | ✅ |
| Credentials | Gmail app password |

---

## 🔗 Connect EKS to ArgoCD

```bash
# Login to ArgoCD
argocd login <argocd-url>:<port> --username admin

# List clusters
argocd cluster list

# Get cluster context
kubectl config get-contexts

# Add cluster
argocd cluster add <cluster-context> --name wanderlust-eks-cluster
```

### Create ArgoCD Application

**Applications** → **New App**

| Setting | Value |
|---------|-------|
| Name | ai-inference |
| Project | default |
| Sync Policy | Automatic |
| Auto-Create Namespace | ✅ |
| Repository URL | Your GitOps repo |
| Path | apps/ai-inference/overlays/dev |
| Cluster | Your EKS cluster |
| Namespace | ai-inference |

---

## 📊 Monitoring with Prometheus and Grafana

### Install Helm

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### Add Repositories

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

### Install Prometheus Stack

```bash
kubectl create namespace prometheus
helm install stable prometheus-community/kube-prometheus-stack -n prometheus
```

### Expose Services

```bash
# Prometheus
kubectl edit svc stable-kube-prometheus-sta-prometheus -n prometheus
# Change type: ClusterIP → type: NodePort

# Grafana
kubectl edit svc stable-grafana -n prometheus
# Change type: ClusterIP → type: NodePort
```

### Get Grafana Password

```bash
kubectl get secret --namespace prometheus stable-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

**Username:** admin

### Recommended Dashboards

| Dashboard ID | Description |
|-------------|-------------|
| 3119 | Kubernetes Cluster Monitoring |
| 6417 | Kubernetes Pod Monitoring |
| 15757 | Kubernetes Views (Global) |

---

## 📁 Project Structure

```
GitOps-Driven-AI-Inference-Platform/
├── gitops-ai-app/                    # Application Source Code
│   ├── src/
│   │   ├── main.py                   # FastAPI entry point
│   │   ├── config.py                 # Configuration
│   │   ├── api/
│   │   │   └── predict.py            # Prediction endpoint
│   │   ├── models/
│   │   │   └── sentiment_model.py    # ML model
│   │   ├── services/
│   │   │   └── inference_service.py  # Business logic
│   │   └── utils/
│   │       └── preprocessing.py      # Text preprocessing
│   ├── tests/                        # Unit tests
│   ├── Dockerfile                    # Multi-stage build
│   ├── Jenkinsfile                   # CI pipeline
│   ├── Jenkinsfile.pr                # PR pipeline
│   └── requirements.txt              # Dependencies
│
├── gitops-manifests/                 # Kubernetes Manifests
│   ├── argocd/
│   │   ├── root-app.yaml             # App of Apps
│   │   └── projects.yaml             # RBAC
│   ├── apps/
│   │   └── ai-inference/
│   │       ├── base/                 # Base manifests
│   │       └── overlays/
│   │           ├── dev/
│   │           ├── staging/
│   │           └── prod/
│   └── monitoring/                   # Prometheus & Grafana
│
└── README.md
```

---

## 🌍 Environments

| Environment | Namespace | Replicas | Auto-Sync |
|-------------|-----------|----------|-----------|
| Dev | ai-inference-dev | 1 | ✅ Yes |
| Staging | ai-inference-staging | 2 | ✅ Yes |
| Production | ai-inference-prod | 3 | ⚠️ Manual |

---

## 🧹 Clean Up

### Delete EKS Cluster

```bash
eksctl delete cluster --name=wanderlust --region=us-west-1
```

### Terminate EC2 Instances

1. AWS Console → EC2 → Instances
2. Select Master & Worker instances
3. Instance State → Terminate

### Clean Docker Resources

```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>Made with ❤️ using GitOps & DevSecOps principles</b>
</p>
